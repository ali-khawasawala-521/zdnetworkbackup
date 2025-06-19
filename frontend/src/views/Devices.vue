<script lang="ts" setup>
import type { Device } from '@/types/device'

import { ref, onMounted } from 'vue'
import { DeviceTable } from '@/components'
import { getDeviceList } from '@/lib/device'

const devices = ref<Device[]>([])

const handleLoadDevices = async () => {
  devices.value = await getDeviceList()
}

onMounted(handleLoadDevices)
</script>

<template>
  <div class="max-w-[1920px] p-4 mx-auto">
    <DeviceTable :devices="devices" @refresh:devices="handleLoadDevices" />
  </div>
</template>

<style></style>
