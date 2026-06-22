# app/logistics/schemas.py

from enum import Enum
from decimal import Decimal
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


# ============================================================
# Enums
# ============================================================

class ShipmentStatus(str, Enum):
    PLANNED = "planned"
    BOOKED = "booked"
    LOADING = "loading"
    LOADED = "loaded"
    IN_TRANSIT = "in_transit"
    ARRIVED = "arrived"
    DISCHARGING = "discharging"
    DISCHARGED = "discharged"
    DELIVERED = "delivered"
    CLOSED = "closed"
    CANCELLED = "cancelled"
    DELAYED = "delayed"
    DISPUTED = "disputed"


class ShipmentMode(str, Enum):
    SEA = "sea"
    ROAD = "road"
    RAIL = "rail"
    AIR = "air"
    MULTIMODAL = "multimodal"


class ShipmentLegMode(str, Enum):
    SEA = "sea"
    ROAD = "road"
    RAIL = "rail"
    AIR = "air"
    BARGE = "barge"
    OTHER = "other"


class ShipmentLegStatus(str, Enum):
    PLANNED = "planned"
    BOOKED = "booked"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DELAYED = "delayed"


class PortType(str, Enum):
    SEAPORT = "seaport"
    AIRPORT = "airport"
    INLAND_PORT = "inland_port"
    TERMINAL = "terminal"
    WAREHOUSE = "warehouse"
    OTHER = "other"


class PortCallType(str, Enum):
    LOADING = "loading"
    DISCHARGE = "discharge"
    TRANSSHIPMENT = "transshipment"
    BUNKERING = "bunkering"
    OTHER = "other"


class PortCallStatus(str, Enum):
    SCHEDULED = "scheduled"
    ARRIVED = "arrived"
    BERTHED = "berthed"
    OPERATIONS_STARTED = "operations_started"
    OPERATIONS_COMPLETED = "operations_completed"
    SAILED = "sailed"
    DELAYED = "delayed"
    CANCELLED = "cancelled"


class LogisticsEventType(str, Enum):
    BOOKING_CONFIRMED = "booking_confirmed"
    CARGO_PICKED_UP = "cargo_picked_up"
    CARGO_ARRIVED_AT_PORT = "cargo_arrived_at_port"
    LOADING_STARTED = "loading_started"
    LOADING_COMPLETED = "loading_completed"
    VESSEL_DEPARTED = "vessel_departed"
    VESSEL_ARRIVED = "vessel_arrived"
    DISCHARGE_STARTED = "discharge_started"
    DISCHARGE_COMPLETED = "discharge_completed"
    CUSTOMS_CLEARED = "customs_cleared"
    CARGO_DELIVERED = "cargo_delivered"
    DELAY_REPORTED = "delay_reported"
    DAMAGE_REPORTED = "damage_reported"
    SHORTAGE_REPORTED = "shortage_reported"
    OTHER = "other"


class LogisticsCostCategory(str, Enum):
    FREIGHT = "freight"
    TRUCKING = "trucking"
    PORT_CHARGES = "port_charges"
    TERMINAL_HANDLING = "terminal_handling"
    STORAGE = "storage"
    WAREHOUSING = "warehousing"
    DEMURRAGE = "demurrage"
    DETENTION = "detention"
    CUSTOMS_CLEARANCE = "customs_clearance"
    SURVEY = "survey"
    OTHER = "other"


class VesselType(str, Enum):
    BULK_CARRIER = "bulk_carrier"
    CONTAINER_SHIP = "container_ship"
    GENERAL_CARGO = "general_cargo"
    TANKER = "tanker"
    BARGE = "barge"
    OTHER = "other"


class ContainerType(str, Enum):
    TWENTY_FOOT = "20ft"
    FORTY_FOOT = "40ft"
    FORTY_FOOT_HC = "40ft_hc"
    OTHER = "other"


class DeliveryOrderStatus(str, Enum):
    DRAFT = "draft"
    ISSUED = "issued"
    PARTIALLY_DELIVERED = "partially_delivered"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class QuantityUnit(str, Enum):
    MT = "mt"
    WMT = "wmt"
    DMT = "dmt"
    KG = "kg"
    LB = "lb"
    UNIT = "unit"
    OTHER = "other"


class WeightUnit(str, Enum):
    MT = "mt"
    KG = "kg"
    LB = "lb"
    OTHER = "other"


# ============================================================
# Shipments
# ============================================================

class ShipmentBase(BaseModel):
    trade_id: Optional[int] = None

    shipment_code: Optional[str] = None
    mode: Optional[ShipmentMode] = ShipmentMode.SEA
    status: Optional[ShipmentStatus] = ShipmentStatus.PLANNED

    logistics_partner_id: Optional[int] = None
    freight_forwarder_id: Optional[int] = None
    carrier_counterparty_id: Optional[int] = None

    origin_location: Optional[str] = None
    destination_location: Optional[str] = None

    origin_port_id: Optional[int] = None
    destination_port_id: Optional[int] = None

    estimated_departure_date: Optional[date] = None
    actual_departure_date: Optional[date] = None

    estimated_arrival_date: Optional[date] = None
    actual_arrival_date: Optional[date] = None

    incoterm: Optional[str] = None

    notes: Optional[str] = None


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentUpdate(BaseModel):
    trade_id: Optional[int] = None

    shipment_code: Optional[str] = None
    mode: Optional[ShipmentMode] = None
    status: Optional[ShipmentStatus] = None

    logistics_partner_id: Optional[int] = None
    freight_forwarder_id: Optional[int] = None
    carrier_counterparty_id: Optional[int] = None

    origin_location: Optional[str] = None
    destination_location: Optional[str] = None

    origin_port_id: Optional[int] = None
    destination_port_id: Optional[int] = None

    estimated_departure_date: Optional[date] = None
    actual_departure_date: Optional[date] = None

    estimated_arrival_date: Optional[date] = None
    actual_arrival_date: Optional[date] = None

    incoterm: Optional[str] = None

    notes: Optional[str] = None


class ShipmentRead(ShipmentBase):
    id: int


# ============================================================
# Cargo
# ============================================================

class CargoBase(BaseModel):
    shipment_id: int
    trade_item_id: Optional[int] = None

    commodity: str
    grade: Optional[str] = None
    description: Optional[str] = None

    package_type: Optional[str] = None
    number_of_packages: Optional[int] = None

    gross_weight: Optional[Decimal] = None
    net_weight: Optional[Decimal] = None
    weight_unit: Optional[WeightUnit] = None

    loaded_quantity: Optional[Decimal] = None
    discharged_quantity: Optional[Decimal] = None
    quantity_unit: Optional[QuantityUnit] = None

    moisture_percentage: Optional[Decimal] = None

    notes: Optional[str] = None


class CargoCreate(CargoBase):
    pass


class CargoUpdate(BaseModel):
    trade_item_id: Optional[int] = None

    commodity: Optional[str] = None
    grade: Optional[str] = None
    description: Optional[str] = None

    package_type: Optional[str] = None
    number_of_packages: Optional[int] = None

    gross_weight: Optional[Decimal] = None
    net_weight: Optional[Decimal] = None
    weight_unit: Optional[WeightUnit] = None

    loaded_quantity: Optional[Decimal] = None
    discharged_quantity: Optional[Decimal] = None
    quantity_unit: Optional[QuantityUnit] = None

    moisture_percentage: Optional[Decimal] = None

    notes: Optional[str] = None


class CargoRead(CargoBase):
    id: int


# ============================================================
# Shipment Legs
# ============================================================

class ShipmentLegBase(BaseModel):
    shipment_id: int

    sequence_number: int
    mode: ShipmentLegMode
    status: Optional[ShipmentLegStatus] = ShipmentLegStatus.PLANNED

    origin_location: Optional[str] = None
    destination_location: Optional[str] = None

    origin_port_id: Optional[int] = None
    destination_port_id: Optional[int] = None

    carrier_counterparty_id: Optional[int] = None
    logistics_partner_id: Optional[int] = None

    vessel_id: Optional[int] = None
    vessel_name: Optional[str] = None

    vehicle_number: Optional[str] = None
    container_id: Optional[int] = None
    container_number: Optional[str] = None

    estimated_departure_time: Optional[datetime] = None
    actual_departure_time: Optional[datetime] = None

    estimated_arrival_time: Optional[datetime] = None
    actual_arrival_time: Optional[datetime] = None

    notes: Optional[str] = None


class ShipmentLegCreate(ShipmentLegBase):
    pass


class ShipmentLegUpdate(BaseModel):
    sequence_number: Optional[int] = None
    mode: Optional[ShipmentLegMode] = None
    status: Optional[ShipmentLegStatus] = None

    origin_location: Optional[str] = None
    destination_location: Optional[str] = None

    origin_port_id: Optional[int] = None
    destination_port_id: Optional[int] = None

    carrier_counterparty_id: Optional[int] = None
    logistics_partner_id: Optional[int] = None

    vessel_id: Optional[int] = None
    vessel_name: Optional[str] = None

    vehicle_number: Optional[str] = None
    container_id: Optional[int] = None
    container_number: Optional[str] = None

    estimated_departure_time: Optional[datetime] = None
    actual_departure_time: Optional[datetime] = None

    estimated_arrival_time: Optional[datetime] = None
    actual_arrival_time: Optional[datetime] = None

    notes: Optional[str] = None


class ShipmentLegRead(ShipmentLegBase):
    id: int


# ============================================================
# Ports
# ============================================================

class PortBase(BaseModel):
    name: str
    country: Optional[str] = None
    city: Optional[str] = None
    unlocode: Optional[str] = None
    port_type: Optional[PortType] = PortType.SEAPORT

    notes: Optional[str] = None


class PortCreate(PortBase):
    pass


class PortUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    unlocode: Optional[str] = None
    port_type: Optional[PortType] = None

    notes: Optional[str] = None


class PortRead(PortBase):
    id: int


# ============================================================
# Port Calls
# ============================================================

class PortCallBase(BaseModel):
    shipment_id: int
    shipment_leg_id: Optional[int] = None

    port_id: int
    port_call_type: PortCallType
    status: Optional[PortCallStatus] = PortCallStatus.SCHEDULED

    eta: Optional[datetime] = None
    ata: Optional[datetime] = None

    etb: Optional[datetime] = None
    atb: Optional[datetime] = None

    operations_start_time: Optional[datetime] = None
    operations_end_time: Optional[datetime] = None

    etd: Optional[datetime] = None
    atd: Optional[datetime] = None

    berth_name: Optional[str] = None
    terminal_name: Optional[str] = None

    notes: Optional[str] = None


class PortCallCreate(PortCallBase):
    pass


class PortCallUpdate(BaseModel):
    shipment_leg_id: Optional[int] = None

    port_id: Optional[int] = None
    port_call_type: Optional[PortCallType] = None
    status: Optional[PortCallStatus] = None

    eta: Optional[datetime] = None
    ata: Optional[datetime] = None

    etb: Optional[datetime] = None
    atb: Optional[datetime] = None

    operations_start_time: Optional[datetime] = None
    operations_end_time: Optional[datetime] = None

    etd: Optional[datetime] = None
    atd: Optional[datetime] = None

    berth_name: Optional[str] = None
    terminal_name: Optional[str] = None

    notes: Optional[str] = None


class PortCallRead(PortCallBase):
    id: int


# ============================================================
# Vessels
# ============================================================

class VesselBase(BaseModel):
    name: str

    imo_number: Optional[str] = None
    mmsi_number: Optional[str] = None
    flag_country: Optional[str] = None

    vessel_type: Optional[VesselType] = None

    deadweight_tonnage: Optional[Decimal] = None
    gross_tonnage: Optional[Decimal] = None

    notes: Optional[str] = None


class VesselCreate(VesselBase):
    pass


class VesselUpdate(BaseModel):
    name: Optional[str] = None

    imo_number: Optional[str] = None
    mmsi_number: Optional[str] = None
    flag_country: Optional[str] = None

    vessel_type: Optional[VesselType] = None

    deadweight_tonnage: Optional[Decimal] = None
    gross_tonnage: Optional[Decimal] = None

    notes: Optional[str] = None


class VesselRead(VesselBase):
    id: int


# ============================================================
# Containers
# ============================================================

class ContainerBase(BaseModel):
    shipment_id: int
    shipment_leg_id: Optional[int] = None

    container_number: str
    seal_number: Optional[str] = None

    container_type: Optional[ContainerType] = None

    tare_weight: Optional[Decimal] = None
    gross_weight: Optional[Decimal] = None
    weight_unit: Optional[WeightUnit] = WeightUnit.KG

    status: Optional[str] = None
    notes: Optional[str] = None


class ContainerCreate(ContainerBase):
    pass


class ContainerUpdate(BaseModel):
    shipment_leg_id: Optional[int] = None

    container_number: Optional[str] = None
    seal_number: Optional[str] = None

    container_type: Optional[ContainerType] = None

    tare_weight: Optional[Decimal] = None
    gross_weight: Optional[Decimal] = None
    weight_unit: Optional[WeightUnit] = None

    status: Optional[str] = None
    notes: Optional[str] = None


class ContainerRead(ContainerBase):
    id: int


# ============================================================
# Logistics Events
# ============================================================

class LogisticsEventBase(BaseModel):
    shipment_id: int
    shipment_leg_id: Optional[int] = None

    event_type: LogisticsEventType
    event_time: Optional[datetime] = None

    location: Optional[str] = None
    port_id: Optional[int] = None

    reported_by_user_id: Optional[int] = None
    counterparty_id: Optional[int] = None

    description: Optional[str] = None
    notes: Optional[str] = None


class LogisticsEventCreate(LogisticsEventBase):
    pass


class LogisticsEventUpdate(BaseModel):
    shipment_leg_id: Optional[int] = None

    event_type: Optional[LogisticsEventType] = None
    event_time: Optional[datetime] = None

    location: Optional[str] = None
    port_id: Optional[int] = None

    reported_by_user_id: Optional[int] = None
    counterparty_id: Optional[int] = None

    description: Optional[str] = None
    notes: Optional[str] = None


class LogisticsEventRead(LogisticsEventBase):
    id: int


# ============================================================
# Logistics Costs
# ============================================================

class LogisticsCostBase(BaseModel):
    shipment_id: int
    shipment_leg_id: Optional[int] = None
    trade_id: Optional[int] = None

    category: LogisticsCostCategory
    description: Optional[str] = None

    counterparty_id: Optional[int] = None

    amount: Decimal
    currency: str

    exchange_rate_to_base: Optional[Decimal] = None
    amount_base_currency: Optional[Decimal] = None

    cost_date: Optional[date] = None
    due_date: Optional[date] = None
    paid_date: Optional[date] = None

    is_estimated: bool = True

    notes: Optional[str] = None


class LogisticsCostCreate(LogisticsCostBase):
    pass


class LogisticsCostUpdate(BaseModel):
    shipment_leg_id: Optional[int] = None
    trade_id: Optional[int] = None

    category: Optional[LogisticsCostCategory] = None
    description: Optional[str] = None

    counterparty_id: Optional[int] = None

    amount: Optional[Decimal] = None
    currency: Optional[str] = None

    exchange_rate_to_base: Optional[Decimal] = None
    amount_base_currency: Optional[Decimal] = None

    cost_date: Optional[date] = None
    due_date: Optional[date] = None
    paid_date: Optional[date] = None

    is_estimated: Optional[bool] = None

    notes: Optional[str] = None


class LogisticsCostRead(LogisticsCostBase):
    id: int


# ============================================================
# Delivery Orders
# ============================================================

class DeliveryOrderBase(BaseModel):
    shipment_id: int
    trade_id: Optional[int] = None

    delivery_order_number: Optional[str] = None
    status: Optional[DeliveryOrderStatus] = DeliveryOrderStatus.DRAFT

    consignee_counterparty_id: Optional[int] = None
    delivery_location: Optional[str] = None

    issued_date: Optional[date] = None
    delivery_deadline: Optional[date] = None
    delivered_date: Optional[date] = None

    quantity: Optional[Decimal] = None
    quantity_unit: Optional[QuantityUnit] = None

    notes: Optional[str] = None


class DeliveryOrderCreate(DeliveryOrderBase):
    pass


class DeliveryOrderUpdate(BaseModel):
    trade_id: Optional[int] = None

    delivery_order_number: Optional[str] = None
    status: Optional[DeliveryOrderStatus] = None

    consignee_counterparty_id: Optional[int] = None
    delivery_location: Optional[str] = None

    issued_date: Optional[date] = None
    delivery_deadline: Optional[date] = None
    delivered_date: Optional[date] = None

    quantity: Optional[Decimal] = None
    quantity_unit: Optional[QuantityUnit] = None

    notes: Optional[str] = None


class DeliveryOrderRead(DeliveryOrderBase):
    id: int


# ============================================================
# Shipment Overview
# ============================================================

class ShipmentOverview(BaseModel):
    shipment: ShipmentRead
    cargo: list[CargoRead] = []
    legs: list[ShipmentLegRead] = []
    events: list[LogisticsEventRead] = []
    costs: list[LogisticsCostRead] = []

from pydantic import BaseModel
from datetime import date
from typing import Optional
from uuid import UUID

class ShipmentBase(BaseModel):
    trade_id: Optional[UUID] = None
    shipment_code: Optional[str] = None
    mode: Optional[str] = None # 'air', 'sea', 'road', 'rail', 'multimodal'
    carrier_name: Optional[str] = None
    freight_forwarder_id: Optional[UUID] = None
    vessel_name: Optional[str] = None
    voyage_number: Optional[str] = None
    bl_number: Optional[str] = None
    container_numbers: Optional[str] = None
    origin_port: Optional[str] = None
    destination_port: Optional[str] = None
    eta: Optional[date] = None
    etd: Optional[date] = None
    actual_arrival_date: Optional[date] = None
    actual_departure_date: Optional[date] = None
    shipment_status: Optional[str] = "planned" # 'planned', 'booked', 'loaded', 'in_transit', 'arrived', 'customs_clearance', 'delivered', 'delayed', 'cancelled'
    notes: Optional[str] = None
