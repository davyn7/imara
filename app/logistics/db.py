# app/logistics/db.py

from collections import Counter
from datetime import date, datetime, timedelta
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
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    return date.fromisoformat(str(value)[:10])


def _parse_datetime(value) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    text = str(value)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    return datetime.fromisoformat(text)


FREIGHT_CATEGORY = "freight"

OPEN_DELIVERY_ORDER_STATUSES = {
    DeliveryOrderStatus.DRAFT.value,
    DeliveryOrderStatus.ISSUED.value,
    DeliveryOrderStatus.PARTIALLY_DELIVERED.value,
}

BOTTLENECK_PORT_CALL_STATUSES = {
    PortCallStatus.BERTHED.value,
    PortCallStatus.OPERATIONS_STARTED.value,
}

IN_TRANSIT_SHIPMENT_STATUSES = {
    ShipmentStatus.LOADED.value,
    ShipmentStatus.IN_TRANSIT.value,
    ShipmentStatus.ARRIVED.value,
    ShipmentStatus.DISCHARGING.value,
    ShipmentStatus.DISCHARGED.value,
}


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


async def _get_all_logistics_costs_db(
    trade_id: int | None = None,
    shipment_id: int | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
):
    if shipment_id is not None:
        costs = await get_logistics_costs_by_shipment_db(shipment_id)
    elif trade_id is not None:
        costs = []
        for shipment in await get_shipments_by_trade_db(trade_id):
            costs.extend(await get_logistics_costs_by_shipment_db(shipment["id"]))
    else:
        costs = supabase.table("logistics_costs").select("*").execute().data

    if from_date is None and to_date is None:
        return costs

    filtered = []
    for cost in costs:
        cost_date = _parse_date(cost.get("cost_date"))
        if from_date is not None and cost_date is not None and cost_date < from_date:
            continue
        if to_date is not None and cost_date is not None and cost_date > to_date:
            continue
        filtered.append(cost)
    return filtered


async def _get_all_delivery_orders_db(trade_id: int | None = None):
    if trade_id is not None:
        orders = []
        for shipment in await get_shipments_by_trade_db(trade_id):
            orders.extend(await get_delivery_orders_by_shipment_db(shipment["id"]))
        return orders
    return supabase.table("delivery_orders").select("*").execute().data


async def _get_all_port_calls_db(trade_id: int | None = None):
    if trade_id is not None:
        port_calls = []
        for shipment in await get_shipments_by_trade_db(trade_id):
            port_calls.extend(
                supabase.table("port_calls")
                .select("*")
                .eq("shipment_id", shipment["id"])
                .execute()
                .data
            )
        return port_calls
    return supabase.table("port_calls").select("*").execute().data


def _aggregate_costs_by_category(costs: list) -> dict:
    by_category: dict[str, dict] = {}
    total_estimated = Decimal("0")
    total_actual = Decimal("0")
    total_paid = Decimal("0")
    total_unpaid = Decimal("0")

    for cost in costs:
        category = cost.get("category") or "other"
        if category not in by_category:
            by_category[category] = {
                "category": category,
                "count": 0,
                "estimated_total": Decimal("0"),
                "actual_total": Decimal("0"),
                "paid_total": Decimal("0"),
                "unpaid_total": Decimal("0"),
                "unpaid_count": 0,
            }

        amount = _amount_in_base(cost)
        entry = by_category[category]
        entry["count"] += 1
        if cost.get("is_estimated"):
            entry["estimated_total"] += amount
            total_estimated += amount
        else:
            entry["actual_total"] += amount
            total_actual += amount
        if cost.get("paid_date"):
            entry["paid_total"] += amount
            total_paid += amount
        else:
            entry["unpaid_total"] += amount
            entry["unpaid_count"] += 1
            total_unpaid += amount

    categories = []
    for category in sorted(by_category):
        entry = by_category[category]
        categories.append(
            {
                "category": entry["category"],
                "count": entry["count"],
                "estimated_total": float(entry["estimated_total"]),
                "actual_total": float(entry["actual_total"]),
                "paid_total": float(entry["paid_total"]),
                "unpaid_total": float(entry["unpaid_total"]),
                "unpaid_count": entry["unpaid_count"],
            }
        )

    return {
        "categories": categories,
        "total_estimated": float(total_estimated),
        "total_actual": float(total_actual),
        "total_paid": float(total_paid),
        "total_unpaid": float(total_unpaid),
        "cost_count": len(costs),
    }


def _planned_cargo_quantity(cargo: dict) -> Decimal:
    for field in ("net_weight", "gross_weight", "loaded_quantity"):
        value = cargo.get(field)
        if value is not None:
            return _to_decimal(value)
    return Decimal("0")


def _port_call_reference_time(port_call: dict) -> datetime | None:
    status = port_call.get("status")
    if status == PortCallStatus.OPERATIONS_STARTED.value:
        return _parse_datetime(port_call.get("operations_start_time"))
    if status == PortCallStatus.BERTHED.value:
        return (
            _parse_datetime(port_call.get("atb"))
            or _parse_datetime(port_call.get("ata"))
            or _parse_datetime(port_call.get("eta"))
        )
    return None


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


async def get_logistics_costs_portfolio_summary_db(
    trade_id: int | None = None,
    shipment_id: int | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
):
    costs = await _get_all_logistics_costs_db(
        trade_id=trade_id,
        shipment_id=shipment_id,
        from_date=from_date,
        to_date=to_date,
    )
    aggregated = _aggregate_costs_by_category(costs)

    return {
        "filters": {
            "trade_id": trade_id,
            "shipment_id": shipment_id,
            "from_date": from_date.isoformat() if from_date else None,
            "to_date": to_date.isoformat() if to_date else None,
        },
        **aggregated,
    }


async def get_open_delivery_orders_summary_db(trade_id: int | None = None):
    today = date.today()
    orders = await _get_all_delivery_orders_db(trade_id)
    open_orders = []

    for order in orders:
        if order.get("status") not in OPEN_DELIVERY_ORDER_STATUSES:
            continue

        deadline = _parse_date(order.get("delivery_deadline"))
        is_overdue = deadline is not None and deadline < today
        open_orders.append(
            {
                **order,
                "is_overdue": is_overdue,
                "days_overdue": (today - deadline).days if is_overdue else 0,
            }
        )

    open_orders.sort(
        key=lambda order: (
            not order["is_overdue"],
            order.get("delivery_deadline") or "9999-12-31",
        )
    )

    return {
        "filters": {"trade_id": trade_id},
        "as_of": today.isoformat(),
        "open_count": len(open_orders),
        "overdue_count": sum(1 for order in open_orders if order["is_overdue"]),
        "by_status": dict(Counter(order.get("status") for order in open_orders)),
        "delivery_orders": open_orders,
    }


async def get_cargo_loading_progress_summary_db(trade_id: int | None = None):
    shipments = await _get_shipments_filtered_db(trade_id)
    rows = []

    for shipment in shipments:
        if not _is_active_shipment(shipment):
            continue

        cargo_items = await get_cargo_by_shipment_db(shipment["id"])
        cargo_rows = []
        total_planned = Decimal("0")
        total_loaded = Decimal("0")
        total_discharged = Decimal("0")

        for cargo in cargo_items:
            planned = _planned_cargo_quantity(cargo)
            loaded = _to_decimal(cargo.get("loaded_quantity"))
            discharged = _to_decimal(cargo.get("discharged_quantity"))
            total_planned += planned
            total_loaded += loaded
            total_discharged += discharged

            loading_progress = (
                float((loaded / planned) * 100) if planned > 0 else None
            )
            discharge_progress = (
                float((discharged / planned) * 100) if planned > 0 else None
            )
            cargo_rows.append(
                {
                    "cargo_id": cargo.get("id"),
                    "commodity": cargo.get("commodity"),
                    "planned_quantity": float(planned),
                    "loaded_quantity": float(loaded),
                    "discharged_quantity": float(discharged),
                    "quantity_unit": cargo.get("quantity_unit")
                    or cargo.get("weight_unit"),
                    "loading_progress_percentage": loading_progress,
                    "discharge_progress_percentage": discharge_progress,
                }
            )

        overall_loading = (
            float((total_loaded / total_planned) * 100) if total_planned > 0 else None
        )
        overall_discharge = (
            float((total_discharged / total_planned) * 100)
            if total_planned > 0
            else None
        )

        rows.append(
            {
                "shipment_id": shipment["id"],
                "shipment_code": shipment.get("shipment_code"),
                "status": shipment.get("status"),
                "overall_loading_progress_percentage": overall_loading,
                "overall_discharge_progress_percentage": overall_discharge,
                "cargo": cargo_rows,
            }
        )

    return {
        "filters": {"trade_id": trade_id},
        "active_shipment_count": len(rows),
        "shipments": rows,
    }


async def get_port_call_bottlenecks_summary_db(
    days_threshold: int = 2,
    trade_id: int | None = None,
):
    now = datetime.now()
    port_calls = await _get_all_port_calls_db(trade_id)
    bottlenecks = []

    for port_call in port_calls:
        if port_call.get("status") not in BOTTLENECK_PORT_CALL_STATUSES:
            continue

        reference_time = _port_call_reference_time(port_call)
        if reference_time is None:
            continue

        if reference_time.tzinfo is not None:
            reference_time = reference_time.replace(tzinfo=None)

        days_stuck = (now - reference_time).total_seconds() / 86400
        if days_stuck < days_threshold:
            continue

        bottlenecks.append(
            {
                **port_call,
                "days_stuck": round(days_stuck, 1),
                "reference_time": reference_time.isoformat(),
            }
        )

    bottlenecks.sort(key=lambda port_call: port_call["days_stuck"], reverse=True)

    return {
        "filters": {
            "trade_id": trade_id,
            "days_threshold": days_threshold,
        },
        "bottleneck_count": len(bottlenecks),
        "by_status": dict(Counter(item.get("status") for item in bottlenecks)),
        "port_calls": bottlenecks,
    }


async def get_shipment_costs_summary_db(shipment_id: int):
    shipment_data = await get_shipment_db(shipment_id)
    if not shipment_data:
        return None

    costs = await get_logistics_costs_by_shipment_db(shipment_id)
    aggregated = _aggregate_costs_by_category(costs)

    return {
        "shipment_id": shipment_id,
        "trade_id": shipment_data[0].get("trade_id"),
        **aggregated,
    }


async def get_shipment_legs_summary_db(shipment_id: int):
    shipment_data = await get_shipment_db(shipment_id)
    if not shipment_data:
        return None

    legs = await get_shipment_legs_db(shipment_id)
    active_legs = [
        leg
        for leg in legs
        if leg.get("status") != ShipmentLegStatus.CANCELLED.value
    ]
    completed_count = sum(
        1
        for leg in active_legs
        if leg.get("status") == ShipmentLegStatus.COMPLETED.value
    )
    delayed_count = sum(
        1
        for leg in active_legs
        if leg.get("status") == ShipmentLegStatus.DELAYED.value
    )
    completion_progress = (
        float(completed_count / len(active_legs)) if active_legs else None
    )

    return {
        "shipment_id": shipment_id,
        "trade_id": shipment_data[0].get("trade_id"),
        "leg_count": len(legs),
        "active_leg_count": len(active_legs),
        "completed_count": completed_count,
        "delayed_count": delayed_count,
        "completion_progress": completion_progress,
        "legs_by_status": dict(Counter(leg.get("status") for leg in legs)),
        "legs_by_mode": dict(Counter(leg.get("mode") for leg in legs)),
    }


async def get_shipment_settlement_status_db(shipment_id: int):
    shipment_data = await get_shipment_db(shipment_id)
    if not shipment_data:
        return None

    shipment = shipment_data[0]
    legs = await get_shipment_legs_db(shipment_id)
    costs = await get_logistics_costs_by_shipment_db(shipment_id)
    delivery_orders = await get_delivery_orders_by_shipment_db(shipment_id)

    active_legs = [
        leg
        for leg in legs
        if leg.get("status") != ShipmentLegStatus.CANCELLED.value
    ]
    incomplete_legs = [
        leg
        for leg in active_legs
        if leg.get("status") != ShipmentLegStatus.COMPLETED.value
    ]
    estimated_costs = [cost for cost in costs if cost.get("is_estimated")]
    unpaid_costs = [cost for cost in costs if not cost.get("paid_date")]
    open_delivery_orders = [
        order
        for order in delivery_orders
        if order.get("status") in OPEN_DELIVERY_ORDER_STATUSES
    ]

    blockers = []
    if shipment.get("status") in TERMINAL_SHIPMENT_STATUSES:
        blockers.append("shipment_already_terminal")
    if incomplete_legs:
        blockers.append("incomplete_legs_remaining")
    if estimated_costs:
        blockers.append("estimated_costs_remaining")
    if unpaid_costs:
        blockers.append("unpaid_costs_remaining")
    if open_delivery_orders:
        blockers.append("open_delivery_orders_remaining")

    return {
        "shipment_id": shipment_id,
        "trade_id": shipment.get("trade_id"),
        "shipment_status": shipment.get("status"),
        "ready_to_close": len(blockers) == 0,
        "blockers": blockers,
        "cost_summary": _shipment_cost_totals(costs),
        "incomplete_leg_count": len(incomplete_legs),
        "open_delivery_order_count": len(open_delivery_orders),
    }


async def get_trade_freight_exposure_summary_db(trade_id: int):
    from app.trades.db import get_trade_costs_by_trade_db

    logistics_estimated = Decimal("0")
    logistics_actual = Decimal("0")
    trade_estimated = Decimal("0")
    trade_actual = Decimal("0")

    for shipment in await get_shipments_by_trade_db(trade_id):
        for cost in await get_logistics_costs_by_shipment_db(shipment["id"]):
            if cost.get("category") != FREIGHT_CATEGORY:
                continue
            amount = _amount_in_base(cost)
            if cost.get("is_estimated"):
                logistics_estimated += amount
            else:
                logistics_actual += amount

    for cost in await get_trade_costs_by_trade_db(trade_id):
        if cost.get("category") != FREIGHT_CATEGORY:
            continue
        amount = _amount_in_base(cost)
        if cost.get("is_estimated"):
            trade_estimated += amount
        else:
            trade_actual += amount

    logistics_total = logistics_estimated + logistics_actual
    trade_total = trade_estimated + trade_actual

    return {
        "trade_id": trade_id,
        "logistics_freight": {
            "estimated": float(logistics_estimated),
            "actual": float(logistics_actual),
            "total": float(logistics_total),
        },
        "trade_freight_costs": {
            "estimated": float(trade_estimated),
            "actual": float(trade_actual),
            "total": float(trade_total),
        },
        "combined_freight_total": float(logistics_total + trade_total),
        "potential_double_count_risk": logistics_total > 0 and trade_total > 0,
        "variance_logistics_vs_trade": float(logistics_total - trade_total),
    }


async def get_trade_logistics_status_db(trade_id: int):
    shipments = await get_shipments_by_trade_db(trade_id)
    shipment_statuses = []
    blockers = set()
    ready_count = 0

    for shipment in shipments:
        status = await get_shipment_settlement_status_db(shipment["id"])
        if not status:
            continue
        shipment_statuses.append(status)
        if status["ready_to_close"]:
            ready_count += 1
        else:
            for blocker in status["blockers"]:
                blockers.add(blocker)

    today = date.today()
    delayed_count = sum(
        1 for shipment in shipments if _is_delayed_shipment(shipment, today)
    )
    open_orders = await get_open_delivery_orders_summary_db(trade_id)

    return {
        "trade_id": trade_id,
        "shipment_count": len(shipments),
        "ready_to_close_shipment_count": ready_count,
        "logistics_ready_to_close": (
            len(shipments) > 0 and ready_count == len(shipments)
        ),
        "delayed_shipment_count": delayed_count,
        "open_delivery_order_count": open_orders["open_count"],
        "overdue_delivery_order_count": open_orders["overdue_count"],
        "aggregate_blockers": sorted(blockers),
        "shipments": shipment_statuses,
    }


async def get_departures_calendar_summary_db(
    from_date: date,
    to_date: date,
    trade_id: int | None = None,
):
    shipments = await _get_shipments_filtered_db(trade_id)
    events = []

    for shipment in shipments:
        for field, event_type in (
            ("estimated_departure_date", "estimated_departure"),
            ("actual_departure_date", "actual_departure"),
        ):
            departure_date = _parse_date(shipment.get(field))
            if departure_date is None:
                continue
            if from_date <= departure_date <= to_date:
                events.append(
                    {
                        "shipment_id": shipment["id"],
                        "trade_id": shipment.get("trade_id"),
                        "shipment_code": shipment.get("shipment_code"),
                        "status": shipment.get("status"),
                        "mode": shipment.get("mode"),
                        "event_type": event_type,
                        "departure_date": departure_date.isoformat(),
                        "origin_location": shipment.get("origin_location"),
                        "destination_location": shipment.get("destination_location"),
                    }
                )

    events.sort(key=lambda event: event["departure_date"])

    return {
        "filters": {
            "trade_id": trade_id,
            "from_date": from_date.isoformat(),
            "to_date": to_date.isoformat(),
        },
        "event_count": len(events),
        "events": events,
    }


async def get_cost_forecast_summary_db(trade_id: int | None = None):
    shipments = await _get_shipments_filtered_db(trade_id)
    in_transit_shipments = [
        shipment
        for shipment in shipments
        if shipment.get("status") in IN_TRANSIT_SHIPMENT_STATUSES
    ]

    total_estimated = Decimal("0")
    total_unpaid_estimated = Decimal("0")
    rows = []

    for shipment in in_transit_shipments:
        costs = await get_logistics_costs_by_shipment_db(shipment["id"])
        shipment_estimated = Decimal("0")
        shipment_unpaid_estimated = Decimal("0")

        for cost in costs:
            if not cost.get("is_estimated"):
                continue
            amount = _amount_in_base(cost)
            shipment_estimated += amount
            if not cost.get("paid_date"):
                shipment_unpaid_estimated += amount

        total_estimated += shipment_estimated
        total_unpaid_estimated += shipment_unpaid_estimated
        rows.append(
            {
                "shipment_id": shipment["id"],
                "shipment_code": shipment.get("shipment_code"),
                "status": shipment.get("status"),
                "estimated_logistics_costs": float(shipment_estimated),
                "unpaid_estimated_logistics_costs": float(shipment_unpaid_estimated),
            }
        )

    return {
        "filters": {"trade_id": trade_id},
        "in_transit_shipment_count": len(in_transit_shipments),
        "total_estimated_logistics_costs": float(total_estimated),
        "total_unpaid_estimated_logistics_costs": float(total_unpaid_estimated),
        "shipments": rows,
    }
