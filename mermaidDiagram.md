```mermaid
sequenceDiagram
  autonumber
  participant U as API Consumer
  participant AS as Address Search Service
  participant CI as Client Identity Service
  participant PC as Product Catalogue Service
  participant CR as Booking References Service
  participant BS as Booking Service

  U->>AS: POST /geocode
  AS-->>U: address by location
  U->>AS: POST /search
  AS-->>U: list of matched addresses
  U->>AS: POST /details
  AS-->>U: address details
  U->>CI: POST /auth
  CI-->>U: client_id
  U->>PC: POST /clients/{client_id}/products/cars
  PC-->>U: list of products with estimates and availability
  U->>CR: GET /clients/{client_id}/booking_references
  CR-->>U: booking references schema
  U->>BS: POST /bookings
  BS-->>U: booking confirmation or failure reason