import type { DeviceForm } from '@/types/device'

const baseUrl = 'http://localhost:6565/device'

export const device_types = [
  { value: 'aruba_os', label: 'Aruba' },
  { value: 'brocade_icx', label: 'Brocade ICX' },
  { value: 'cisco_ios', label: 'Cisco IOS' },
  { value: 'dell_force10', label: 'Dell Force10' },
  { value: 'fortinet', label: 'Fortinet' },
  { value: 'huawei', label: 'Huawei' },
  { value: 'juniper', label: 'Juniper' },
  { value: 'paloalto_panos', label: 'Palo Alto' },
  { value: 'ruijie', label: 'Ruijie' },
]

export const get_device_type = (type: string) => {
  const deviceType = device_types.find((device) => device.value === type)
  return deviceType ? deviceType.label : 'Unknown'
}

export const addDevice = async (data: DeviceForm) => {
  console.log({ data })
  try {
    const response = await fetch(`${baseUrl}/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })

    if (!response.ok) throw new Error('Cannot add device')

    return response.json()
  } catch (error) {
    console.error('Error:', error)
    throw error
  }
}

export const editDevice = async (id: string | number, data: DeviceForm) => {
  try {
    const response = await fetch(`${baseUrl}/${id}`, {
      method: 'PUT',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })

    if (!response.ok) throw new Error('Cannot add device')

    return response.json()
  } catch (error) {
    console.error('Error:', error)
    throw error
  }
}

export const getDevice = async (id: string | number) => {
  try {
    const response = await fetch(`${baseUrl}/${id}`, {
      method: 'GET',
      credentials: 'include',
    })

    if (!response.ok) throw new Error('Cannot fetch device')

    return response.json()
  } catch (error) {
    console.error('Error:', error)
    throw error
  }
}

export const getDeviceList = async () => {
  try {
    const response = await fetch(`${baseUrl}/list`, {
      method: 'GET',
      credentials: 'include',
    })

    if (!response.ok) throw new Error('Cannot fetch devices')

    return response.json()
  } catch (error) {
    console.error('Error:', error)
    throw error
  }
}

export const deleteDevice = async (id: string | number) => {
  try {
    const response = await fetch(`${baseUrl}/${id}`, {
      method: 'DELETE',
      credentials: 'include',
    })

    if (!response.ok) throw new Error('Cannot delete device')

    return response.json()
  } catch (error) {
    console.error('Error:', error)
    throw error
  }
}

export const addBackup = async (device_id: string | number) => {
  try {
    const response = await fetch(`${baseUrl}/${device_id}/backup`, {
      method: 'POST',
      credentials: 'include',
    })

    if (!response.ok) throw new Error('Cannot add backup')

    return response.json()
  } catch (error) {
    console.error('Error:', error)
    throw error
  }
}
