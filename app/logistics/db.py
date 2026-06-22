# app/logistics/db.py

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
)


def _serialize(model) -> dict:
    return model.model_dump(mode="json")


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
    events = (
        supabase.table("logistics_events")
        .select("*")
        .eq("shipment_id", shipment_id)
        .execute()
        .data
    )
    costs = (
        supabase.table("logistics_costs")
        .select("*")
        .eq("shipment_id", shipment_id)
        .execute()
        .data
    )

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
