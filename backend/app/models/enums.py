import enum


class UserRole(str, enum.Enum):
    CUSTOMER = "CUSTOMER"
    TECHNICIAN = "TECHNICIAN"
    MERCHANT = "MERCHANT"
    AGENCY = "AGENCY"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


class CertificateStatus(str, enum.Enum):
    NOT_PROVIDED = "NOT_PROVIDED"
    PENDING_REVIEW = "PENDING_REVIEW"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class JobStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    ON_THE_WAY = "ON_THE_WAY"
    ARRIVED = "ARRIVED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    DISPUTED = "DISPUTED"


class InfrastructureMode(str, enum.Enum):
    FREE = "FREE"
    SCALING_REVIEW = "SCALING_REVIEW"
    PRODUCTION = "PRODUCTION"


class ThemeName(str, enum.Enum):
    CLASSIC = "classic"
    OCEAN = "ocean"
    FOREST = "forest"
    SUNSET = "sunset"
    MIDNIGHT = "midnight"


class AppearanceMode(str, enum.Enum):
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"

class JobStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    ON_THE_WAY = "ON_THE_WAY"
    ARRIVED = "ARRIVED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    DISPUTED = "DISPUTED"


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PAID = "PAID"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"


class MediaType(str, enum.Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    DOCUMENT = "DOCUMENT"
    OTHER = "OTHER"


class MediaOwnerType(str, enum.Enum):
    USER = "USER"
    JOB = "JOB"
    SPARE_PART = "SPARE_PART"
    CERTIFICATE = "CERTIFICATE"
    REVIEW = "REVIEW"