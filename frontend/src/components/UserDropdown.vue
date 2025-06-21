<script setup lang="ts">
import type { User } from '@/types/user'

import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Icon } from '@iconify/vue'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
} from '@/components/ui/dropdown-menu'
import { CreateUserDialog } from '@/components'
import { logout } from '@/lib/auth'
import { scheduler_status, start_scheduler, stop_scheduler } from '@/lib/scheduler'

const router = useRouter()

const showUserModal = ref<boolean>(false)
const user = ref<User | null>(JSON.parse(localStorage.getItem('user') || '{}'))
const schedulerStatus = ref<string | null>(null)

const logoutUser = async () => {
  await logout()
  await router.push('/login')
}

const handleStartScheduler = async () => {
  await start_scheduler()
  schedulerStatus.value = 'active'
}

const handleStopScheduler = async () => {
  await stop_scheduler()
  schedulerStatus.value = 'inactive'
}

onMounted(async () => {
  const scheduler = await scheduler_status()
  schedulerStatus.value = scheduler.active ? 'active' : 'inactive'
})
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button variant="outline">
        <Icon icon="radix-icons:person" class="h-[1.2rem] w-[1.2rem]" />
        {{ user?.email || '' }}
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent align="end">
      <DropdownMenuItem @click="showUserModal = true">
        <Icon icon="radix-icons:plus" /> Create New User
      </DropdownMenuItem>
      <DropdownMenuSub>
        <DropdownMenuSubTrigger>
          <div class="flex items-center justify-center gap-3">
            <Icon icon="radix-icons:clock" />
            <span>Schedule Backup</span>
          </div>
        </DropdownMenuSubTrigger>
        <DropdownMenuPortal>
          <DropdownMenuSubContent>
            <DropdownMenuItem
              v-if="schedulerStatus === 'active'"
              variant="destructive"
              @click="handleStopScheduler"
            >
              <span>Stop</span>
            </DropdownMenuItem>
            <DropdownMenuItem v-else @click="handleStartScheduler">
              <span>Start</span>
            </DropdownMenuItem>
          </DropdownMenuSubContent>
        </DropdownMenuPortal>
      </DropdownMenuSub>
      <Separator />
      <DropdownMenuItem variant="destructive" @click="logoutUser">
        <Icon icon="radix-icons:exit" /> Logout
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
  <CreateUserDialog v-model:show="showUserModal" />
</template>

<style scoped></style>
