<script setup lang="ts">
import { useVModel } from '@vueuse/core'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'

const props = defineProps<{
  open?: boolean
  title: string
  description: string
  hideCancel?: boolean
}>()

const emits = defineEmits<{
  (e: 'update:open', value: boolean): void
  (e: 'on:cancel'): void
  (e: 'on:ok'): void
}>()

const showModal = useVModel(props, 'open', emits)
</script>

<template>
  <AlertDialog v-model:open="showModal">
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle>{{ title }}</AlertDialogTitle>
        <AlertDialogDescription>
          {{ description }}
        </AlertDialogDescription>
      </AlertDialogHeader>
      <AlertDialogFooter>
        <AlertDialogCancel v-if="!hideCancel" @click="emits('on:cancel')">Cancel</AlertDialogCancel>
        <AlertDialogAction @click="emits('on:ok')">Continue</AlertDialogAction>
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
</template>
