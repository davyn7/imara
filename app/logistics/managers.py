# app/logistics/managers.py

from app.logistics.schemas import (
    ShipmentCreate,
    ShipmentUpdate,
    CargoCreate,
    CargoUpdate,
    CargoLoadedQuantityUpdate,
    CargoDischargedQuantityUpdate,
    ShipmentLegCreate,
    ShipmentLegUpdate,
    PortCreate,
    PortUpdate,
    PortCallCreate,
    PortCallUpdate,
)
from app.logistics.db import (
    get_shipments_db,
    get_shipment_db,
    get_shipments_by_trade_db,
    add_shipment_db,
    update_shipment_db,
    delete_shipment_db,
    book_shipment_db,
    mark_shipment_as_loading_db,
    mark_shipment_as_loaded_db,
    mark_shipment_as_in_transit_db,
    mark_shipment_as_arrived_db,
    mark_shipment_as_discharged_db,
    mark_shipment_as_delivered_db,
    close_shipment_db,
    cancel_shipment_db,
    delay_shipment_db,
    get_shipment_overview_db,
    get_cargo_by_shipment_db,
    get_cargo_db,
    add_cargo_db,
    update_cargo_db,
    delete_cargo_db,
    update_cargo_loaded_quantity_db,
    update_cargo_discharged_quantity_db,
    get_shipment_legs_db,
    get_shipment_leg_db,
    add_shipment_leg_db,
    update_shipment_leg_db,
    delete_shipment_leg_db,
    start_shipment_leg_db,
    complete_shipment_leg_db,
    delay_shipment_leg_db,
    cancel_shipment_leg_db,
    get_ports_db,
    get_port_db,
    add_port_db,
    update_port_db,
    delete_port_db,
    get_port_calls_by_shipment_db,
    get_port_call_db,
    add_port_call_db,
    update_port_call_db,
    delete_port_call_db,
    mark_port_call_as_arrived_db,
    mark_port_call_as_berthed_db,
    start_port_call_operations_db,
    complete_port_call_operations_db,
    mark_port_call_as_sailed_db,
)


class ShipmentManager:
    def __init__(self, shipment: ShipmentCreate | ShipmentUpdate | None = None):
        self.shipment = shipment

    async def get_shipments(self):
        return await get_shipments_db()

    async def get_shipment(self, shipment_id: int):
        return await get_shipment_db(shipment_id)

    async def get_shipments_by_trade(self, trade_id: int):
        return await get_shipments_by_trade_db(trade_id)

    async def create_shipment(self):
        return await add_shipment_db(self.shipment)

    async def update_shipment(self, shipment_id: int):
        return await update_shipment_db(self.shipment, shipment_id)

    async def delete_shipment(self, shipment_id: int):
        return await delete_shipment_db(shipment_id)

    async def book_shipment(self, shipment_id: int):
        return await book_shipment_db(shipment_id)

    async def mark_shipment_as_loading(self, shipment_id: int):
        return await mark_shipment_as_loading_db(shipment_id)

    async def mark_shipment_as_loaded(self, shipment_id: int):
        return await mark_shipment_as_loaded_db(shipment_id)

    async def mark_shipment_as_in_transit(self, shipment_id: int):
        return await mark_shipment_as_in_transit_db(shipment_id)

    async def mark_shipment_as_arrived(self, shipment_id: int):
        return await mark_shipment_as_arrived_db(shipment_id)

    async def mark_shipment_as_discharged(self, shipment_id: int):
        return await mark_shipment_as_discharged_db(shipment_id)

    async def mark_shipment_as_delivered(self, shipment_id: int):
        return await mark_shipment_as_delivered_db(shipment_id)

    async def close_shipment(self, shipment_id: int):
        return await close_shipment_db(shipment_id)

    async def cancel_shipment(self, shipment_id: int):
        return await cancel_shipment_db(shipment_id)

    async def delay_shipment(self, shipment_id: int):
        return await delay_shipment_db(shipment_id)

    async def get_shipment_overview(self, shipment_id: int):
        return await get_shipment_overview_db(shipment_id)


class CargoManager:
    def __init__(self, cargo: CargoCreate | CargoUpdate | None = None):
        self.cargo = cargo

    async def get_cargo_by_shipment(self, shipment_id: int):
        return await get_cargo_by_shipment_db(shipment_id)

    async def get_cargo(self, cargo_id: int):
        return await get_cargo_db(cargo_id)

    async def create_cargo(self, shipment_id: int):
        return await add_cargo_db(shipment_id, self.cargo)

    async def update_cargo(self, cargo_id: int):
        return await update_cargo_db(self.cargo, cargo_id)

    async def delete_cargo(self, cargo_id: int):
        return await delete_cargo_db(cargo_id)

    async def update_cargo_loaded_quantity(
        self,
        cargo_id: int,
        update: CargoLoadedQuantityUpdate,
    ):
        return await update_cargo_loaded_quantity_db(cargo_id, update)

    async def update_cargo_discharged_quantity(
        self,
        cargo_id: int,
        update: CargoDischargedQuantityUpdate,
    ):
        return await update_cargo_discharged_quantity_db(cargo_id, update)


class ShipmentLegManager:
    def __init__(
        self,
        shipment_leg: ShipmentLegCreate | ShipmentLegUpdate | None = None,
    ):
        self.shipment_leg = shipment_leg

    async def get_shipment_legs(self, shipment_id: int):
        return await get_shipment_legs_db(shipment_id)

    async def get_shipment_leg(self, shipment_leg_id: int):
        return await get_shipment_leg_db(shipment_leg_id)

    async def create_shipment_leg(self, shipment_id: int):
        return await add_shipment_leg_db(shipment_id, self.shipment_leg)

    async def update_shipment_leg(self, shipment_leg_id: int):
        return await update_shipment_leg_db(self.shipment_leg, shipment_leg_id)

    async def delete_shipment_leg(self, shipment_leg_id: int):
        return await delete_shipment_leg_db(shipment_leg_id)

    async def start_shipment_leg(self, shipment_leg_id: int):
        return await start_shipment_leg_db(shipment_leg_id)

    async def complete_shipment_leg(self, shipment_leg_id: int):
        return await complete_shipment_leg_db(shipment_leg_id)

    async def delay_shipment_leg(self, shipment_leg_id: int):
        return await delay_shipment_leg_db(shipment_leg_id)

    async def cancel_shipment_leg(self, shipment_leg_id: int):
        return await cancel_shipment_leg_db(shipment_leg_id)


class PortManager:
    def __init__(self, port: PortCreate | PortUpdate | None = None):
        self.port = port

    async def get_ports(self):
        return await get_ports_db()

    async def get_port(self, port_id: int):
        return await get_port_db(port_id)

    async def create_port(self):
        return await add_port_db(self.port)

    async def update_port(self, port_id: int):
        return await update_port_db(self.port, port_id)

    async def delete_port(self, port_id: int):
        return await delete_port_db(port_id)


class PortCallManager:
    def __init__(self, port_call: PortCallCreate | PortCallUpdate | None = None):
        self.port_call = port_call

    async def get_port_calls_by_shipment(self, shipment_id: int):
        return await get_port_calls_by_shipment_db(shipment_id)

    async def get_port_call(self, port_call_id: int):
        return await get_port_call_db(port_call_id)

    async def create_port_call(self, shipment_id: int):
        return await add_port_call_db(shipment_id, self.port_call)

    async def update_port_call(self, port_call_id: int):
        return await update_port_call_db(self.port_call, port_call_id)

    async def delete_port_call(self, port_call_id: int):
        return await delete_port_call_db(port_call_id)

    async def mark_port_call_as_arrived(self, port_call_id: int):
        return await mark_port_call_as_arrived_db(port_call_id)

    async def mark_port_call_as_berthed(self, port_call_id: int):
        return await mark_port_call_as_berthed_db(port_call_id)

    async def start_port_call_operations(self, port_call_id: int):
        return await start_port_call_operations_db(port_call_id)

    async def complete_port_call_operations(self, port_call_id: int):
        return await complete_port_call_operations_db(port_call_id)

    async def mark_port_call_as_sailed(self, port_call_id: int):
        return await mark_port_call_as_sailed_db(port_call_id)
