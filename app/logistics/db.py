# app/logistics/db.py

from collections import Counter
from datetime import date, timedelta
from decimal import Decimal

from app.connection import supabase
from app.logistics.schemas import (
    ShipmentCreate,
    ShipmentUpdate,
    ShipmentStatus,
    CargoCreate,
    CargoUpdate,
    CargoLoadedQuantityUpdate,
    CargoDischargedQuantityUpdate,
    ShipmentLegCreate,
    ShipmentLegUpdate,
    ShipmentLegStatus,
    PortCreate,
    PortUpdate,
    PortCallCreate,
    PortCallUpdate,
    PortCallStatus,
    VesselCreate,
    VesselUpdate,
    ContainerCreate,
    ContainerUpdate,
    LogisticsEventCreate,
    LogisticsEventUpdate,
    LogisticsCostCreate,
    LogisticsCostUpdate,
    DeliveryOrderCreate,
    DeliveryOrderUpdate,
    DeliveryOrderStatus,
)


def _serialize(model) -> dict:
    return model.model_dump(mode="json")


def _to_decimal(value) -> Decimal:
    if value is None:
        return Decimal("0")
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def _amount_in_base(record: dict) -> Decimal:
    base_amount = record.get("amount_base_currency")
    if base_amount is not None:
        return _to_decimal(base_amount)
    return _to_decimal(record.get("amount"))


def _parse_date(value) -> date | None:
    if value is None:
        return None
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


TERMINAL_SHIPMENT_STATUSES = {
    ShipmentStatus.CLOSED.value,
    ShipmentStatus.CANCELLED.value,
}

DELIVERED_SHIPMENT_STATUSES = {
    ShipmentStatus.DELIVERED.value,
    ShipmentStatus.CLOSED.value,
}


async def _get_shipments_filtered_db(trade_id: int | None = None):
    query = supabase.table("shipments").select("*")
    if trade_id is not None:
        query = query.eq("trade_id", trade_id)
    return query.execute().data


def _is_active_shipment(shipment: dict) -> bool:
    return shipment.get("status") not in TERMINAL_SHIPMENT_STATUSES


def _is_delayed_shipment(shipment: dict, today: date) -> bool:
    if shipment.get("status") == ShipmentStatus.DELAYED.value:
        return True

    status = shipment.get("status")
    if status in TERMINAL_SHIPMENT_STATUSES or status in DELIVERED_SHIPMENT_STATUSES:
        return False

    estimated_arrival = _parse_date(shipment.get("estimated_arrival_date"))
    if estimated_arrival is not None and estimated_arrival < today:
        return True

    estimated_departure = _parse_date(shipment.get("estimated_departure_date"))
    if (
        estimated_departure is not None
        and estimated_departure < today
        and status in {
            ShipmentStatus.PLANNED.value,
            ShipmentStatus.BOOKED.value,
            ShipmentStatus.LOADING.value,
        }
    ):
        return True

    return False


def _shipment_cost_totals(costs: list) -> dict:
    estimated = Decimal("0")
    actual = Decimal("0")
    unpaid = Decimal("0")

    for cost in costs:
        amount = _amount_in_base(cost)
        if cost.get("is_estimated"):
            estimated += amount
        else:
            actual += amount
        if not cost.get("paid_date"):
            unpaid += amount

    return {
        "estimated": float(estimated),
        "actual": float(actual),
        "unpaid": float(unpaid),
    }


async def _serialize_shipment_logistics_row(shipment: dict) -> dict:
    shipment_id = shipment["id"]
    legs = await get_shipment_legs_db(shipment_id)
    cargo = await get_cargo_by_shipment_db(shipment_id)
    costs = await get_logistics_costs_by_shipment_db(shipment_id)
    events = await get_logistics_events_by_shipment_db(shipment_id)
    delivery_orders = await get_delivery_orders_by_shipment_db(shipment_id)
    cost_totals = _shipment_cost_totals(costs)

    return {
        "shipment_id": shipment_id,
        "trade_id": shipment.get("trade_id"),
        "shipment_code": shipment.get("shipment_code"),
        "status": shipment.get("status"),
        "mode": shipment.get("mode"),
        "origin_location": shipment.get("origin_location"),
        "destination_location": shipment.get("destination_location"),
        "estimated_departure_date": shipment.get("estimated_departure_date"),
        "estimated_arrival_date": shipment.get("estimated_arrival_date"),
        "actual_departure_date": shipment.get("actual_departure_date"),
        "actual_arrival_date": shipment.get("actual_arrival_date"),
        "counts": {
            "legs": len(legs),
            "cargo": len(cargo),
            "costs": len(costs),
            "events": len(events),
            "delivery_orders": len(delivery_orders),
        },
        "legs_by_status": dict(Counter(leg.get("status") for leg in legs)),
        "delivery_orders_by_status": dict(
            Counter(order.get("status") for order in delivery_orders)
        ),
        "cost_totals": cost_totals,
        "recent_events": events[-5:],
    }


async def _update_shipment_status_db(shipment_id: int, status: ShipmentStatus):
    response = (
        supabase.table("shipments")
        .update({"status": status.value})
        .eq("id", shipment_id)
        .execute()
    )
    return response.data


# Shipment DB Operations

async def get_shipments_db():
    response = supabase.table("shipments").select("*").execute()
    return response.data


async def get_shipment_db(shipment_id: int):
    response = (
        supabase.table("shipments")
        .select("*")
        .eq("id", shipment_id)
        .execute()
    )
    return response.data


async def get_shipments_by_trade_db(trade_id: int):
    response = (
        supabase.table("shipments")
        .select("*")
        .eq("trade_id", trade_id)
        .execute()
    )
    return response.data


async def add_shipment_db(shipment: ShipmentCreate):
    shipment_data = _serialize(shipment)
    response = supabase.table("shipments").insert(shipment_data).execute()
    return response.data


async def update_shipment_db(shipment: ShipmentUpdate, shipment_id: int):
    shipment_data = shipment.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("shipments")
        .update(shipment_data)
        .eq("id", shipment_id)
        .execute()
    )
    return response.data


async def delete_shipment_db(shipment_id: int):
    response = (
        supabase.table("shipments")
        .delete()
        .eq("id", shipment_id)
        .execute()
    )
    return response.data


async def book_shipment_db(shipment_id: int):
    return await _update_shipment_status_db(shipment_id, ShipmentStatus.BOOKED)


async def mark_shipment_as_loading_db(shipment_id: int):
    return await _update_shipment_status_db(shipment_id, ShipmentStatus.LOADING)


async def mark_shipment_as_loaded_db(shipment_id: int):
    return await _update_shipment_status_db(shipment_id, ShipmentStatus.LOADED)


async def mark_shipment_as_in_transit_db(shipment_id: int):
    return await _update_shipment_status_db(shipment_id, ShipmentStatus.IN_TRANSIT)


async def mark_shipment_as_arrived_db(shipment_id: int):
    return await _update_shipment_status_db(shipment_id, ShipmentStatus.ARRIVED)


async def mark_shipment_as_discharged_db(shipment_id: int):
    return await _update_shipment_status_db(shipment_id, ShipmentStatus.DISCHARGED)


async def mark_shipment_as_delivered_db(shipment_id: int):
    return await _update_shipment_status_db(shipment_id, ShipmentStatus.DELIVERED)


async def close_shipment_db(shipment_id: int):
    return await _update_shipment_status_db(shipment_id, ShipmentStatus.CLOSED)


async def cancel_shipment_db(shipment_id: int):
    return await _update_shipment_status_db(shipment_id, ShipmentStatus.CANCELLED)


async def delay_shipment_db(shipment_id: int):
    return await _update_shipment_status_db(shipment_id, ShipmentStatus.DELAYED)


async def get_shipment_overview_db(shipment_id: int):
    shipment_data = await get_shipment_db(shipment_id)
    if not shipment_data:
        return None

    cargo = await get_cargo_by_shipment_db(shipment_id)
    legs = await get_shipment_legs_db(shipment_id)
    events = await get_logistics_events_by_shipment_db(shipment_id)
    costs = await get_logistics_costs_by_shipment_db(shipment_id)

    return {
        "shipment": shipment_data[0],
        "cargo": cargo,
        "legs": legs,
        "events": events,
        "costs": costs,
    }


# Cargo DB Operations

async def get_cargo_by_shipment_db(shipment_id: int):
    response = (
        supabase.table("cargo")
        .select("*")
        .eq("shipment_id", shipment_id)
        .execute()
    )
    return response.data


async def get_cargo_db(cargo_id: int):
    response = (
        supabase.table("cargo")
        .select("*")
        .eq("id", cargo_id)
        .execute()
    )
    return response.data


async def add_cargo_db(shipment_id: int, cargo: CargoCreate):
    cargo_data = _serialize(cargo)
    cargo_data["shipment_id"] = shipment_id
    response = supabase.table("cargo").insert(cargo_data).execute()
    return response.data


async def update_cargo_db(cargo: CargoUpdate, cargo_id: int):
    cargo_data = cargo.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("cargo")
        .update(cargo_data)
        .eq("id", cargo_id)
        .execute()
    )
    return response.data


async def delete_cargo_db(cargo_id: int):
    response = (
        supabase.table("cargo")
        .delete()
        .eq("id", cargo_id)
        .execute()
    )
    return response.data


async def update_cargo_loaded_quantity_db(
    cargo_id: int,
    update: CargoLoadedQuantityUpdate,
):
    update_data = update.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("cargo")
        .update(update_data)
        .eq("id", cargo_id)
        .execute()
    )
    return response.data


async def update_cargo_discharged_quantity_db(
    cargo_id: int,
    update: CargoDischargedQuantityUpdate,
):
    update_data = update.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("cargo")
        .update(update_data)
        .eq("id", cargo_id)
        .execute()
    )
    return response.data


async def _update_shipment_leg_status_db(
    shipment_leg_id: int,
    status: ShipmentLegStatus,
):
    response = (
        supabase.table("shipment_legs")
        .update({"status": status.value})
        .eq("id", shipment_leg_id)
        .execute()
    )
    return response.data


# Shipment Leg DB Operations

async def get_shipment_legs_db(shipment_id: int):
    response = (
        supabase.table("shipment_legs")
        .select("*")
        .eq("shipment_id", shipment_id)
        .execute()
    )
    return response.data


async def get_shipment_leg_db(shipment_leg_id: int):
    response = (
        supabase.table("shipment_legs")
        .select("*")
        .eq("id", shipment_leg_id)
        .execute()
    )
    return response.data


async def add_shipment_leg_db(shipment_id: int, shipment_leg: ShipmentLegCreate):
    shipment_leg_data = _serialize(shipment_leg)
    shipment_leg_data["shipment_id"] = shipment_id
    response = supabase.table("shipment_legs").insert(shipment_leg_data).execute()
    return response.data


async def update_shipment_leg_db(
    shipment_leg: ShipmentLegUpdate,
    shipment_leg_id: int,
):
    shipment_leg_data = shipment_leg.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("shipment_legs")
        .update(shipment_leg_data)
        .eq("id", shipment_leg_id)
        .execute()
    )
    return response.data


async def delete_shipment_leg_db(shipment_leg_id: int):
    response = (
        supabase.table("shipment_legs")
        .delete()
        .eq("id", shipment_leg_id)
        .execute()
    )
    return response.data


async def start_shipment_leg_db(shipment_leg_id: int):
    return await _update_shipment_leg_status_db(
        shipment_leg_id,
        ShipmentLegStatus.IN_PROGRESS,
    )


async def complete_shipment_leg_db(shipment_leg_id: int):
    return await _update_shipment_leg_status_db(
        shipment_leg_id,
        ShipmentLegStatus.COMPLETED,
    )


async def delay_shipment_leg_db(shipment_leg_id: int):
    return await _update_shipment_leg_status_db(
        shipment_leg_id,
        ShipmentLegStatus.DELAYED,
    )


async def cancel_shipment_leg_db(shipment_leg_id: int):
    return await _update_shipment_leg_status_db(
        shipment_leg_id,
        ShipmentLegStatus.CANCELLED,
    )


# Port DB Operations

async def get_ports_db():
    response = supabase.table("ports").select("*").execute()
    return response.data


async def get_port_db(port_id: int):
    response = (
        supabase.table("ports")
        .select("*")
        .eq("id", port_id)
        .execute()
    )
    return response.data


async def add_port_db(port: PortCreate):
    port_data = _serialize(port)
    response = supabase.table("ports").insert(port_data).execute()
    return response.data


async def update_port_db(port: PortUpdate, port_id: int):
    port_data = port.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("ports")
        .update(port_data)
        .eq("id", port_id)
        .execute()
    )
    return response.data


async def delete_port_db(port_id: int):
    response = (
        supabase.table("ports")
        .delete()
        .eq("id", port_id)
        .execute()
    )
    return response.data


async def _update_port_call_status_db(port_call_id: int, status: PortCallStatus):
    response = (
        supabase.table("port_calls")
        .update({"status": status.value})
        .eq("id", port_call_id)
        .execute()
    )
    return response.data


# Port Call DB Operations

async def get_port_calls_by_shipment_db(shipment_id: int):
    response = (
        supabase.table("port_calls")
        .select("*")
        .eq("shipment_id", shipment_id)
        .execute()
    )
    return response.data


async def get_port_call_db(port_call_id: int):
    response = (
        supabase.table("port_calls")
        .select("*")
        .eq("id", port_call_id)
        .execute()
    )
    return response.data


async def add_port_call_db(shipment_id: int, port_call: PortCallCreate):
    port_call_data = _serialize(port_call)
    port_call_data["shipment_id"] = shipment_id
    response = supabase.table("port_calls").insert(port_call_data).execute()
    return response.data


async def update_port_call_db(port_call: PortCallUpdate, port_call_id: int):
    port_call_data = port_call.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("port_calls")
        .update(port_call_data)
        .eq("id", port_call_id)
        .execute()
    )
    return response.data


async def delete_port_call_db(port_call_id: int):
    response = (
        supabase.table("port_calls")
        .delete()
        .eq("id", port_call_id)
        .execute()
    )
    return response.data


async def mark_port_call_as_arrived_db(port_call_id: int):
    return await _update_port_call_status_db(port_call_id, PortCallStatus.ARRIVED)


async def mark_port_call_as_berthed_db(port_call_id: int):
    return await _update_port_call_status_db(port_call_id, PortCallStatus.BERTHED)


async def start_port_call_operations_db(port_call_id: int):
    return await _update_port_call_status_db(
        port_call_id,
        PortCallStatus.OPERATIONS_STARTED,
    )


async def complete_port_call_operations_db(port_call_id: int):
    return await _update_port_call_status_db(
        port_call_id,
        PortCallStatus.OPERATIONS_COMPLETED,
    )


async def mark_port_call_as_sailed_db(port_call_id: int):
    return await _update_port_call_status_db(port_call_id, PortCallStatus.SAILED)


# Vessel DB Operations

async def get_vessels_db():
    response = supabase.table("vessels").select("*").execute()
    return response.data


async def get_vessel_db(vessel_id: int):
    response = (
        supabase.table("vessels")
        .select("*")
        .eq("id", vessel_id)
        .execute()
    )
    return response.data


async def add_vessel_db(vessel: VesselCreate):
    vessel_data = _serialize(vessel)
    response = supabase.table("vessels").insert(vessel_data).execute()
    return response.data


async def update_vessel_db(vessel: VesselUpdate, vessel_id: int):
    vessel_data = vessel.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("vessels")
        .update(vessel_data)
        .eq("id", vessel_id)
        .execute()
    )
    return response.data


async def delete_vessel_db(vessel_id: int):
    response = (
        supabase.table("vessels")
        .delete()
        .eq("id", vessel_id)
        .execute()
    )
    return response.data


# Container DB Operations

async def get_containers_by_shipment_db(shipment_id: int):
    response = (
        supabase.table("containers")
        .select("*")
        .eq("shipment_id", shipment_id)
        .execute()
    )
    return response.data


async def get_container_db(container_id: int):
    response = (
        supabase.table("containers")
        .select("*")
        .eq("id", container_id)
        .execute()
    )
    return response.data


async def add_container_db(shipment_id: int, container: ContainerCreate):
    container_data = _serialize(container)
    container_data["shipment_id"] = shipment_id
    response = supabase.table("containers").insert(container_data).execute()
    return response.data


async def update_container_db(container: ContainerUpdate, container_id: int):
    container_data = container.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("containers")
        .update(container_data)
        .eq("id", container_id)
        .execute()
    )
    return response.data


async def delete_container_db(container_id: int):
    response = (
        supabase.table("containers")
        .delete()
        .eq("id", container_id)
        .execute()
    )
    return response.data


# Logistics Event DB Operations

async def get_logistics_events_by_shipment_db(shipment_id: int):
    response = (
        supabase.table("logistics_events")
        .select("*")
        .eq("shipment_id", shipment_id)
        .execute()
    )
    return response.data


async def get_logistics_event_db(event_id: int):
    response = (
        supabase.table("logistics_events")
        .select("*")
        .eq("id", event_id)
        .execute()
    )
    return response.data


async def add_logistics_event_db(shipment_id: int, event: LogisticsEventCreate):
    event_data = _serialize(event)
    event_data["shipment_id"] = shipment_id
    response = supabase.table("logistics_events").insert(event_data).execute()
    return response.data


async def update_logistics_event_db(event: LogisticsEventUpdate, event_id: int):
    event_data = event.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("logistics_events")
        .update(event_data)
        .eq("id", event_id)
        .execute()
    )
    return response.data


async def delete_logistics_event_db(event_id: int):
    response = (
        supabase.table("logistics_events")
        .delete()
        .eq("id", event_id)
        .execute()
    )
    return response.data


# Logistics Cost DB Operations

async def get_logistics_costs_by_shipment_db(shipment_id: int):
    response = (
        supabase.table("logistics_costs")
        .select("*")
        .eq("shipment_id", shipment_id)
        .execute()
    )
    return response.data


async def get_logistics_cost_db(cost_id: int):
    response = (
        supabase.table("logistics_costs")
        .select("*")
        .eq("id", cost_id)
        .execute()
    )
    return response.data


async def add_logistics_cost_db(shipment_id: int, cost: LogisticsCostCreate):
    cost_data = _serialize(cost)
    cost_data["shipment_id"] = shipment_id
    response = supabase.table("logistics_costs").insert(cost_data).execute()
    return response.data


async def update_logistics_cost_db(cost: LogisticsCostUpdate, cost_id: int):
    cost_data = cost.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("logistics_costs")
        .update(cost_data)
        .eq("id", cost_id)
        .execute()
    )
    return response.data


async def delete_logistics_cost_db(cost_id: int):
    response = (
        supabase.table("logistics_costs")
        .delete()
        .eq("id", cost_id)
        .execute()
    )
    return response.data


async def mark_logistics_cost_as_actual_db(cost_id: int):
    response = (
        supabase.table("logistics_costs")
        .update({"is_estimated": False})
        .eq("id", cost_id)
        .execute()
    )
    return response.data


async def mark_logistics_cost_as_paid_db(cost_id: int):
    response = (
        supabase.table("logistics_costs")
        .update({"paid_date": date.today().isoformat()})
        .eq("id", cost_id)
        .execute()
    )
    return response.data


async def _update_delivery_order_status_db(
    delivery_order_id: int,
    status: DeliveryOrderStatus,
    extra_fields: dict | None = None,
):
    update_data = {"status": status.value}
    if extra_fields:
        update_data.update(extra_fields)
    response = (
        supabase.table("delivery_orders")
        .update(update_data)
        .eq("id", delivery_order_id)
        .execute()
    )
    return response.data


# Delivery Order DB Operations

async def get_delivery_orders_by_shipment_db(shipment_id: int):
    response = (
        supabase.table("delivery_orders")
        .select("*")
        .eq("shipment_id", shipment_id)
        .execute()
    )
    return response.data


async def get_delivery_order_db(delivery_order_id: int):
    response = (
        supabase.table("delivery_orders")
        .select("*")
        .eq("id", delivery_order_id)
        .execute()
    )
    return response.data


async def add_delivery_order_db(shipment_id: int, delivery_order: DeliveryOrderCreate):
    delivery_order_data = _serialize(delivery_order)
    delivery_order_data["shipment_id"] = shipment_id
    response = supabase.table("delivery_orders").insert(delivery_order_data).execute()
    return response.data


async def update_delivery_order_db(
    delivery_order: DeliveryOrderUpdate,
    delivery_order_id: int,
):
    delivery_order_data = delivery_order.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("delivery_orders")
        .update(delivery_order_data)
        .eq("id", delivery_order_id)
        .execute()
    )
    return response.data


async def delete_delivery_order_db(delivery_order_id: int):
    response = (
        supabase.table("delivery_orders")
        .delete()
        .eq("id", delivery_order_id)
        .execute()
    )
    return response.data


async def issue_delivery_order_db(delivery_order_id: int):
    return await _update_delivery_order_status_db(
        delivery_order_id,
        DeliveryOrderStatus.ISSUED,
        {"issued_date": date.today().isoformat()},
    )


async def mark_delivery_order_as_delivered_db(delivery_order_id: int):
    return await _update_delivery_order_status_db(
        delivery_order_id,
        DeliveryOrderStatus.DELIVERED,
        {"delivered_date": date.today().isoformat()},
    )


async def cancel_delivery_order_db(delivery_order_id: int):
    return await _update_delivery_order_status_db(
        delivery_order_id,
        DeliveryOrderStatus.CANCELLED,
    )


# Logistics Summary DB Operations

async def get_active_shipments_summary_db(trade_id: int | None = None):
    shipments = await _get_shipments_filtered_db(trade_id)
    active = [shipment for shipment in shipments if _is_active_shipment(shipment)]

    return {
        "filters": {"trade_id": trade_id},
        "active_count": len(active),
        "by_status": dict(Counter(shipment.get("status") for shipment in active)),
        "by_mode": dict(Counter(shipment.get("mode") for shipment in active)),
        "shipments": active,
    }


async def get_delayed_shipments_summary_db(trade_id: int | None = None):
    today = date.today()
    shipments = await _get_shipments_filtered_db(trade_id)
    delayed = [
        shipment for shipment in shipments if _is_delayed_shipment(shipment, today)
    ]

    return {
        "filters": {"trade_id": trade_id},
        "as_of": today.isoformat(),
        "delayed_count": len(delayed),
        "by_status": dict(Counter(shipment.get("status") for shipment in delayed)),
        "shipments": delayed,
    }


async def get_upcoming_arrivals_summary_db(
    days: int = 14,
    trade_id: int | None = None,
):
    today = date.today()
    end_date = today + timedelta(days=days)
    shipments = await _get_shipments_filtered_db(trade_id)

    upcoming = []
    for shipment in shipments:
        if shipment.get("status") in TERMINAL_SHIPMENT_STATUSES:
            continue

        estimated_arrival = _parse_date(shipment.get("estimated_arrival_date"))
        if estimated_arrival is None:
            continue
        if today <= estimated_arrival <= end_date:
            upcoming.append(shipment)

    upcoming.sort(key=lambda shipment: shipment.get("estimated_arrival_date") or "")

    return {
        "filters": {
            "trade_id": trade_id,
            "days": days,
        },
        "window_start": today.isoformat(),
        "window_end": end_date.isoformat(),
        "upcoming_count": len(upcoming),
        "shipments": upcoming,
    }


async def get_shipments_by_status_summary_db(trade_id: int | None = None):
    shipments = await _get_shipments_filtered_db(trade_id)

    return {
        "filters": {"trade_id": trade_id},
        "total_count": len(shipments),
        "by_status": dict(Counter(shipment.get("status") for shipment in shipments)),
        "by_mode": dict(Counter(shipment.get("mode") for shipment in shipments)),
    }


async def get_trade_logistics_summary_db(trade_id: int):
    shipments = await get_shipments_by_trade_db(trade_id)
    shipment_rows = []
    total_estimated_costs = Decimal("0")
    total_actual_costs = Decimal("0")
    total_unpaid_costs = Decimal("0")

    for shipment in shipments:
        row = await _serialize_shipment_logistics_row(shipment)
        shipment_rows.append(row)
        total_estimated_costs += Decimal(str(row["cost_totals"]["estimated"]))
        total_actual_costs += Decimal(str(row["cost_totals"]["actual"]))
        total_unpaid_costs += Decimal(str(row["cost_totals"]["unpaid"]))

    active_count = sum(1 for shipment in shipments if _is_active_shipment(shipment))
    delayed_count = sum(
        1 for shipment in shipments if _is_delayed_shipment(shipment, date.today())
    )

    return {
        "trade_id": trade_id,
        "shipment_count": len(shipments),
        "active_shipment_count": active_count,
        "delayed_shipment_count": delayed_count,
        "shipments_by_status": dict(
            Counter(shipment.get("status") for shipment in shipments)
        ),
        "shipments_by_mode": dict(
            Counter(shipment.get("mode") for shipment in shipments)
        ),
        "total_estimated_logistics_costs": float(total_estimated_costs),
        "total_actual_logistics_costs": float(total_actual_costs),
        "total_unpaid_logistics_costs": float(total_unpaid_costs),
        "shipments": shipment_rows,
    }
