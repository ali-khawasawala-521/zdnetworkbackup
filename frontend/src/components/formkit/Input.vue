<script setup>
import { Input } from '@/components/ui/input'
const props = defineProps({
  context: Object,
})
</script>

<template>
  <Input
    :model-value="context._value"
    @update:model-value="props.context.node.input"
    :type="context.type || 'text'"
    :placeholder="context.placeholder"
    class="min-w-xs"
  />
</template>
