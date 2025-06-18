<script setup lang="ts">
import { useVModel } from '@vueuse/core'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogTitle,
  DialogHeader,
  DialogFooter,
} from '@/components/ui/dialog'
import { formatLocaleDate } from '@/lib/helper'

const props = defineProps<{
  show: boolean
  backup: any
}>()

const emit = defineEmits<{
  (e: 'update:show', value: boolean): void
}>()

const showModal = useVModel(props, 'show', emit)
</script>

<template>
  <Dialog v-model:open="showModal">
    <DialogContent class="sm:max-w-[425px]">
      <DialogHeader>
        <DialogTitle>Backup</DialogTitle>
        <DialogDescription>
          Configuration Backup for {{ backup.hostname }} <{{ backup.ip_address }}>
        </DialogDescription>
      </DialogHeader>
      <pre>{{ backup.config }}</pre>
    </DialogContent>
  </Dialog>
</template>

<style scoped></style>
