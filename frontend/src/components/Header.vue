<script lang="ts" setup>
import { useRouter } from 'vue-router'
import { DarkModeToggle, UserDropdown } from '@/components'
import { Button } from '@/components/ui/button'
import { logout } from '@/lib/auth'
import Logo from '@/assets/logo.svg'
</script>

<template>
  <header class="flex justify-between items-center px-4 shadow-md min-h-[70px]">
    <div>
      <Logo class="w-12 h-12" />
    </div>

    <div class="flex justify-center items-center gap-4">
      <nav class="flex justify-center items-center gap-2">
        <router-link to="/">
          <Button variant="ghost">Devices</Button>
        </router-link>
        <router-link to="/backups">
          <Button variant="ghost">Backups</Button>
        </router-link>
      </nav>
      <DarkModeToggle />
      <UserDropdown />
    </div>
  </header>
</template>

<style></style>
