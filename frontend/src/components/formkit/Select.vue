<script setup>
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
const props = defineProps({
  context: Object,
})

console.log(props.context)
</script>

<template>
  <Select :model-value="context._value" @update:model-value="props.context.node.input">
    <SelectTrigger class="w-xs">
      <SelectValue :placeholder="context.placeholder" />
    </SelectTrigger>
    <SelectContent>
      <SelectGroup>
        <SelectLabel>{{ context.selectLabel }}</SelectLabel>
        <SelectItem v-for="opt in context.selectOptions" :value="opt.value">
          {{ opt.label }}
        </SelectItem>
      </SelectGroup>
    </SelectContent>
  </Select>
</template>
