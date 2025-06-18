<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { FormKit } from '@formkit/vue'
import { Loader2 } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter,
} from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { login } from '@/lib/auth'

const router = useRouter()

const isLoading = ref<boolean>(false)

const onSubmit = async (formData: any) => {
  try {
    isLoading.value = true
    await login(formData)
    router.push({ name: 'devices' })
  } catch (error) {
    console.error(error)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <Card>
      <CardHeader>
        <CardTitle>Login to your account</CardTitle>
        <CardDescription> Enter your email below to login to your account </CardDescription>
      </CardHeader>
      <CardContent>
        <FormKit type="form" :actions="false" @submit="onSubmit">
          <div class="flex flex-col items-center justify-center gap-2">
            <div class="flex flex-col">
              <Label for="email">Email</Label>
              <FormKit
                type="email"
                name="email"
                validation="required|email"
                validation-visibility="dirty"
              />
            </div>
            <div class="flex flex-col">
              <div class="flex items-center">
                <Label for="password">Password</Label>
              </div>
              <FormKit
                type="password"
                name="password"
                validation="length:8|required"
                validation-visibility="dirty"
              />
            </div>
            <Button type="submit" class="w-full" :disabled="isLoading">
              <span v-if="isLoading">
                <Loader2 class="w-4 h-4 mr-2 animate-spin" />
                Please wait
              </span>
              <span v-else>Login</span>
            </Button>
          </div>
        </FormKit>
      </CardContent>
      <CardFooter class="flex justify-center items-center">
        <p>Powered by <a href="https://zamarmardesign.com" target="_blank">ZD</a></p>
      </CardFooter>
    </Card>
  </div>
</template>
