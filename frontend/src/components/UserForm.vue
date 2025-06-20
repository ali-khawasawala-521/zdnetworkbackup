<script setup lang="ts">
import { ref } from 'vue'
import { FormKit } from '@formkit/vue'
import { reset } from '@formkit/core'
import { toast } from 'vue-sonner'
import { Button } from '@/components/ui/button'
import { register } from '@/lib/auth'

const emit = defineEmits(['success'])

const isLoading = ref<boolean>(false)

const handleSubmit = async (formData: any) => {
  if (formData.password !== formData.confirm_password) {
    toast.warning('Passwords do not match')
    return
  }

  const payload = {
    email: formData.email,
    password: formData.password,
  }

  isLoading.value = true
  await register(payload)
  reset('user-form')
  isLoading.value = false
  emit('success')
}
</script>

<template>
  <FormKit id="user-form" type="form" :actions="false" @submit="handleSubmit">
    <div class="flex flex-col items-center justify-center gap-2">
      <FormKit
        type="email"
        label="Email"
        name="email"
        validation="required|email"
        validation-visibility="dirty"
      />
      <FormKit
        type="password"
        label="Password"
        name="password"
        validation="required"
        validation-visibility="dirty"
      />
      <FormKit
        type="password"
        label="Confirm Password"
        name="confirm_password"
        validation="required"
        validation-visibility="dirty"
      />
      <Button type="submit">Create New User</Button>
    </div>
  </FormKit>
</template>

<style scoped></style>
