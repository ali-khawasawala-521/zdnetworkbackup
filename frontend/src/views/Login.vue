<script lang="ts" setup>
import { LoginForm, DarkModeToggle } from '@/components'
import { isAuthenticated, logout } from '@/lib/auth'
</script>

<template>
  <div class="h-screen flex items-center justify-center p-4">
    <LoginForm class="min-w-sm" />
  </div>
</template>

<style></style>
