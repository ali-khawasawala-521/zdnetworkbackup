<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'
import 'vue-sonner/style.css'
import { Toaster } from '@/components/ui/sonner'
import { Header, Footer } from '@/components'

const route = useRoute()
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <Header v-if="route.path !== '/login'" />
    <main class="grow-2">
      <RouterView />
    </main>
    <Footer v-if="route.path !== '/login'" />
  </div>
  <Toaster richColors position="top-right" />
</template>
