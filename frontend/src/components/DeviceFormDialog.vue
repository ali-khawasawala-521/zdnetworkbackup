<script setup lang="ts">
import type { DeviceForm as DeviceFormType } from '@/types/device'

import { useVModel } from '@vueuse/core'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { DeviceForm } from '@/components'

type DeviceFormWithId = DeviceFormType & { id: string }

const props = defineProps<{
  show: boolean
  deviceData: DeviceFormWithId | null
}>()

const emits = defineEmits<{
  (e: 'update:open', value: boolean): void
  (e: 'success'): void
  (e: 'error', error: any): void
}>()

const showModal = useVModel(props, 'show', emits)
</script>

<template>
  <Dialog v-model:open="showModal">
    <DialogTrigger as-child> </DialogTrigger>
    <DialogContent class="sm:max-w-[425px]">
      <DialogHeader>
        <DialogTitle>Add Device</DialogTitle>
        <DialogDescription>Add device and backup configuration</DialogDescription>
        <div class="my-2"></div>
        <DeviceForm
          :deviceData="deviceData"
          @success="emits('success')"
          @error="emits('error', $event)"
        />
      </DialogHeader>
    </DialogContent>
  </Dialog>
</template>

<style scoped></style>
