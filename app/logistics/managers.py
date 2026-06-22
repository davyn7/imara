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
    get_vessels_db,
    get_vessel_db,
    add_vessel_db,
    update_vessel_db,
    delete_vessel_db,
    get_containers_by_shipment_db,
    get_container_db,
    add_container_db,
    update_container_db,
    delete_container_db,
    get_logistics_events_by_shipment_db,
    get_logistics_event_db,
    add_logistics_event_db,
    update_logistics_event_db,
    delete_logistics_event_db,
    get_logistics_costs_by_shipment_db,
    get_logistics_cost_db,
    add_logistics_cost_db,
    update_logistics_cost_db,
    delete_logistics_cost_db,
    mark_logistics_cost_as_actual_db,
    mark_logistics_cost_as_paid_db,
    get_delivery_orders_by_shipment_db,
    get_delivery_order_db,
    add_delivery_order_db,
    update_delivery_order_db,
    delete_delivery_order_db,
    issue_delivery_order_db,
    mark_delivery_order_as_delivered_db,
    cancel_delivery_order_db,
    get_active_shipments_summary_db,
    get_delayed_shipments_summary_db,
    get_upcoming_arrivals_summary_db,
    get_shipments_by_status_summary_db,
    get_trade_logistics_summary_db,
    get_logistics_costs_portfolio_summary_db,
    get_open_delivery_orders_summary_db,
    get_cargo_loading_progress_summary_db,
    get_port_call_bottlenecks_summary_db,
    get_shipment_costs_summary_db,
    get_shipment_legs_summary_db,
    get_shipment_settlement_status_db,
    get_trade_freight_exposure_summary_db,
    get_trade_logistics_status_db,
    get_departures_calendar_summary_db,
    get_cost_forecast_summary_db,
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


class VesselManager:
    def __init__(self, vessel: VesselCreate | VesselUpdate | None = None):
        self.vessel = vessel

    async def get_vessels(self):
        return await get_vessels_db()

    async def get_vessel(self, vessel_id: int):
        return await get_vessel_db(vessel_id)

    async def create_vessel(self):
        return await add_vessel_db(self.vessel)

    async def update_vessel(self, vessel_id: int):
        return await update_vessel_db(self.vessel, vessel_id)

    async def delete_vessel(self, vessel_id: int):
        return await delete_vessel_db(vessel_id)


class ContainerManager:
    def __init__(self, container: ContainerCreate | ContainerUpdate | None = None):
        self.container = container

    async def get_containers_by_shipment(self, shipment_id: int):
        return await get_containers_by_shipment_db(shipment_id)

    async def get_container(self, container_id: int):
        return await get_container_db(container_id)

    async def create_container(self, shipment_id: int):
        return await add_container_db(shipment_id, self.container)

    async def update_container(self, container_id: int):
        return await update_container_db(self.container, container_id)

    async def delete_container(self, container_id: int):
        return await delete_container_db(container_id)


class LogisticsEventManager:
    def __init__(
        self,
        event: LogisticsEventCreate | LogisticsEventUpdate | None = None,
    ):
        self.event = event

    async def get_logistics_events_by_shipment(self, shipment_id: int):
        return await get_logistics_events_by_shipment_db(shipment_id)

    async def get_logistics_event(self, event_id: int):
        return await get_logistics_event_db(event_id)

    async def create_logistics_event(self, shipment_id: int):
        return await add_logistics_event_db(shipment_id, self.event)

    async def update_logistics_event(self, event_id: int):
        return await update_logistics_event_db(self.event, event_id)

    async def delete_logistics_event(self, event_id: int):
        return await delete_logistics_event_db(event_id)


class LogisticsCostManager:
    def __init__(
        self,
        cost: LogisticsCostCreate | LogisticsCostUpdate | None = None,
    ):
        self.cost = cost

    async def get_logistics_costs_by_shipment(self, shipment_id: int):
        return await get_logistics_costs_by_shipment_db(shipment_id)

    async def get_logistics_cost(self, cost_id: int):
        return await get_logistics_cost_db(cost_id)

    async def create_logistics_cost(self, shipment_id: int):
        return await add_logistics_cost_db(shipment_id, self.cost)

    async def update_logistics_cost(self, cost_id: int):
        return await update_logistics_cost_db(self.cost, cost_id)

    async def delete_logistics_cost(self, cost_id: int):
        return await delete_logistics_cost_db(cost_id)

    async def mark_logistics_cost_as_actual(self, cost_id: int):
        return await mark_logistics_cost_as_actual_db(cost_id)

    async def mark_logistics_cost_as_paid(self, cost_id: int):
        return await mark_logistics_cost_as_paid_db(cost_id)


class DeliveryOrderManager:
    def __init__(
        self,
        delivery_order: DeliveryOrderCreate | DeliveryOrderUpdate | None = None,
    ):
        self.delivery_order = delivery_order

    async def get_delivery_orders_by_shipment(self, shipment_id: int):
        return await get_delivery_orders_by_shipment_db(shipment_id)

    async def get_delivery_order(self, delivery_order_id: int):
        return await get_delivery_order_db(delivery_order_id)

    async def create_delivery_order(self, shipment_id: int):
        return await add_delivery_order_db(shipment_id, self.delivery_order)

    async def update_delivery_order(self, delivery_order_id: int):
        return await update_delivery_order_db(self.delivery_order, delivery_order_id)

    async def delete_delivery_order(self, delivery_order_id: int):
        return await delete_delivery_order_db(delivery_order_id)

    async def issue_delivery_order(self, delivery_order_id: int):
        return await issue_delivery_order_db(delivery_order_id)

    async def mark_delivery_order_as_delivered(self, delivery_order_id: int):
        return await mark_delivery_order_as_delivered_db(delivery_order_id)

    async def cancel_delivery_order(self, delivery_order_id: int):
        return await cancel_delivery_order_db(delivery_order_id)


class LogisticsSummaryManager:
    async def get_active_shipments_summary(self, trade_id: int | None = None):
        return await get_active_shipments_summary_db(trade_id)

    async def get_delayed_shipments_summary(self, trade_id: int | None = None):
        return await get_delayed_shipments_summary_db(trade_id)

    async def get_upcoming_arrivals_summary(
        self,
        days: int = 14,
        trade_id: int | None = None,
    ):
        return await get_upcoming_arrivals_summary_db(days, trade_id)

    async def get_shipments_by_status_summary(self, trade_id: int | None = None):
        return await get_shipments_by_status_summary_db(trade_id)

    async def get_trade_logistics_summary(self, trade_id: int):
        return await get_trade_logistics_summary_db(trade_id)

    async def get_logistics_costs_portfolio_summary(
        self,
        trade_id: int | None = None,
        shipment_id: int | None = None,
        from_date=None,
        to_date=None,
    ):
        return await get_logistics_costs_portfolio_summary_db(
            trade_id,
            shipment_id,
            from_date,
            to_date,
        )

    async def get_open_delivery_orders_summary(self, trade_id: int | None = None):
        return await get_open_delivery_orders_summary_db(trade_id)

    async def get_cargo_loading_progress_summary(self, trade_id: int | None = None):
        return await get_cargo_loading_progress_summary_db(trade_id)

    async def get_port_call_bottlenecks_summary(
        self,
        days_threshold: int = 2,
        trade_id: int | None = None,
    ):
        return await get_port_call_bottlenecks_summary_db(days_threshold, trade_id)

    async def get_shipment_costs_summary(self, shipment_id: int):
        return await get_shipment_costs_summary_db(shipment_id)

    async def get_shipment_legs_summary(self, shipment_id: int):
        return await get_shipment_legs_summary_db(shipment_id)

    async def get_shipment_settlement_status(self, shipment_id: int):
        return await get_shipment_settlement_status_db(shipment_id)

    async def get_trade_freight_exposure_summary(self, trade_id: int):
        return await get_trade_freight_exposure_summary_db(trade_id)

    async def get_trade_logistics_status(self, trade_id: int):
        return await get_trade_logistics_status_db(trade_id)

    async def get_departures_calendar_summary(
        self,
        from_date,
        to_date,
        trade_id: int | None = None,
    ):
        return await get_departures_calendar_summary_db(from_date, to_date, trade_id)

    async def get_cost_forecast_summary(self, trade_id: int | None = None):
        return await get_cost_forecast_summary_db(trade_id)
