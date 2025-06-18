<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { FormKit } from '@formkit/vue'
import { Loader2 } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { device_types, addDevice, editDevice } from '@/lib/device'

import type { DeviceForm } from '@/types/device'

const { deviceData } = defineProps<{
  deviceData?: (DeviceForm & { id: string }) | null
}>()

const emit = defineEmits<{
  (event: 'success'): void
  (event: 'error', err: any): void
}>()

const deviceForm = ref<DeviceForm>({
  ip_address: '',
  username: '',
  password: '',
  enable_password: '',
  device_type: '',
})

const isLoading = ref<boolean>(false)

const mode = computed(() => (deviceData ? 'edit' : 'add'))

const onSubmit = async (data: DeviceForm) => {
  try {
    isLoading.value = true
    if (mode.value === 'edit' && deviceData?.id) {
      await editDevice(deviceData.id, data)
    } else {
      await addDevice(data)
    }
    emit('success')
  } catch (err) {
    emit('error', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  if (deviceData) {
    deviceForm.value = deviceData
  }
})
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-2">
    <FormKit type="form" :actions="false" v-model:model-value="deviceForm" @submit="onSubmit">
      <div class="flex flex-col">
        <Label for="ip_address">IP Address</Label>
        <FormKit
          type="text"
          name="ip_address"
          validation="required"
          validation-visibility="dirty"
        />
      </div>
      <div class="flex flex-col">
        <Label for="username">Username</Label>
        <FormKit type="text" name="username" validation="required" validation-visibility="dirty" />
      </div>
      <div class="flex flex-col">
        <Label for="password">Password</Label>
        <FormKit
          type="text"
          name="password"
          :validation="mode === 'add' ? 'required' : ''"
          validation-visibility="dirty"
          :help="mode === 'edit' ? 'Leave blank if you do not want to change the password' : ''"
        />
      </div>
      <div class="flex flex-col">
        <Label for="enable_password">Secret</Label>
        <FormKit
          type="text"
          name="enable_password"
          :help="
            mode === 'edit' ? 'Leave blank if you do not want to change the enable password' : ''
          "
        />
      </div>
      <div class="flex flex-col">
        <Label for="device_type">Device Type</Label>
        <FormKit
          type="select"
          name="device_type"
          selectLabel="Select Device Type"
          placeholder="Select Device Type"
          :selectOptions="device_types"
          validation="required"
          validation-visibility="dirty"
        />
      </div>
      <Button type="submit" class="w-full" :disabled="isLoading">
        <span v-if="isLoading">
          <Loader2 class="w-4 h-4 mr-2 animate-spin" />
          Please wait
        </span>
        <span v-else>{{ mode === 'add' ? 'Add' : 'Update' }} Device</span>
      </Button>
    </FormKit>
  </div>
</template>

<style></style>
