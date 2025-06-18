export interface DeviceForm {
  ip_address: string
  username: string
  password: string
  enable_password?: string
  device_type: string
}

export interface Device {
  id: string
  device_type: string
  ip_address: string
  hostname: string
  username: string
  created_at: string
  total_backups: number
}
