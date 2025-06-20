<script setup lang="ts">
import { useVModel } from '@vueuse/core'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { UserForm } from './index'

const props = defineProps<{
  show: boolean
}>()

const emit = defineEmits<{
  (e: 'update:show', value: boolean): void
  (e: 'user:created'): void
}>()

const showModal = useVModel(props, 'show', emit)
</script>

<template>
  <Dialog v-model:open="showModal">
    <DialogTrigger as-child> </DialogTrigger>
    <DialogContent class="sm:max-w-[400px]">
      <DialogHeader>
        <DialogTitle>Create New User</DialogTitle>
        <div class="my-2"></div>
        <UserForm @success="showModal = false" />
      </DialogHeader>
    </DialogContent>
  </Dialog>
</template>
