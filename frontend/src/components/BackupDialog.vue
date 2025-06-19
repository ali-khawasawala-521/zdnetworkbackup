<script setup lang="ts">
import { useVModel } from '@vueuse/core'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogTitle,
  DialogHeader,
} from '@/components/ui/dialog'

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
    <DialogContent class="sm:max-w-[800px]">
      <DialogHeader>
        <DialogTitle>Backup</DialogTitle>
        <DialogDescription>
          Configuration Backup for {{ backup.hostname }} <{{ backup.ip_address }}>
        </DialogDescription>
      </DialogHeader>
      <pre class="overflow-auto max-h-[600px]">{{ backup.config }}</pre>
    </DialogContent>
  </Dialog>
</template>

<style scoped></style>
