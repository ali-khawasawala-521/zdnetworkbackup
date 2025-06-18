<script setup lang="ts">
import type { Device, DeviceForm } from '@/types/device'

import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Loader2 } from 'lucide-vue-next'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { DeviceFormDialog, AlertDialog } from '@/components'
import { getDeviceList, deleteDevice, addBackup, get_device_type } from '@/lib/device'
import { formatLocaleDate } from '@/lib/helper'

type DeviceFormWithId = DeviceForm & { id: string }

const router = useRouter()

const loadingBackup = ref<string | null>(null)
const deviceModal = ref<boolean>(false)
const alertModal = ref<boolean>(false)
const devices = ref<Device[]>([])
const selectedDevice = ref<DeviceFormWithId | null>(null)

const handleEditDevice = async (device: Device) => {
  selectedDevice.value = device as unknown as DeviceFormWithId
  deviceModal.value = true
}

const handleGetBackup = async (device: Device) => {
  try {
    loadingBackup.value = device.id
    await addBackup(device.id)
  } finally {
    loadingBackup.value = null
  }
  // Show success message or update UI
}

const handleShowDeviceBackups = async (device: Device) => {
  router.push({ name: 'backups', params: { id: device.id } })
}

const handleAskDeleteDevice = async (device: Device) => {
  selectedDevice.value = device as unknown as DeviceFormWithId
  alertModal.value = true
}

const handleDeleteDevice = async (device: Device) => {
  await deleteDevice(device.id)
  await handleLoadDevices()
  selectedDevice.value = null
}

const handleLoadDevices = async () => {
  devices.value = await getDeviceList()
}

const handleDevice = async (error?: any) => {
  if (error) {
    console.error('Error adding device:', error)
    return
  }
  deviceModal.value = false
  await handleLoadDevices()
}

watch(deviceModal, () => {
  if (!deviceModal.value) {
    selectedDevice.value = null
  }
})

onMounted(async () => {
  await handleLoadDevices()
})
</script>

<template>
  <Card>
    <CardHeader class="flex justify-between items-center gap-4">
      <CardTitle>Devices</CardTitle>
      <Button @click="deviceModal = true"> Add Device </Button>
    </CardHeader>
    <CardContent>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>Device Type</TableHead>
            <TableHead>IP Address</TableHead>
            <TableHead>Hostname</TableHead>
            <TableHead>Username</TableHead>
            <TableHead>Created At</TableHead>
            <TableHead>Total Backups</TableHead>
            <TableHead class="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow v-for="device in devices" :key="device.id">
            <TableCell>{{ device.id }}</TableCell>
            <TableCell>{{ get_device_type(device.device_type) }}</TableCell>
            <TableCell>{{ device.ip_address }}</TableCell>
            <TableCell>{{ device.hostname }}</TableCell>
            <TableCell>{{ device.username }}</TableCell>
            <TableCell>{{ formatLocaleDate(device.created_at) }}</TableCell>
            <TableCell>{{ device.total_backups }}</TableCell>
            <TableCell class="text-right">
              <div class="flex items-center justify-end gap-2">
                <Button
                  size="sm"
                  @click="handleGetBackup(device)"
                  :disabled="loadingBackup === device.id"
                >
                  <Loader2 v-if="loadingBackup === device.id" class="mr-2 animate-spin" />
                  <span>Get Backup</span>
                </Button>
                <Button size="sm" @click="handleShowDeviceBackups(device)"
                  >Show Devices Backups</Button
                >
                <Button size="sm" @click="handleEditDevice(device)">Edit Device</Button>
                <Button size="sm" variant="destructive" @click="handleAskDeleteDevice(device)"
                  >Delete Device</Button
                >
              </div>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </CardContent>
  </Card>
  <DeviceFormDialog
    v-model:show="deviceModal"
    :deviceData="selectedDevice"
    @success="handleDevice"
    @error="handleDevice"
  />
  <AlertDialog
    v-model:open="alertModal"
    title="Are you sure?"
    description="It will remove your device and all its backups. This action cannot be undone."
    @on:ok="handleDeleteDevice(selectedDevice as unknown as Device)"
  />
</template>
