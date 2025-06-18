<script setup lang="ts">
import { useVModel } from '@vueuse/core'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogTitle,
  DialogHeader,
} from '@/components/ui/dialog'
import { ScrollArea } from '@/components/ui/scroll-area'

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
      <ScrollArea class="w-full h-[600px]">
        <p>{{ backup.config }}</p>
      </ScrollArea>
    </DialogContent>
  </Dialog>
</template>

<style scoped></style>
