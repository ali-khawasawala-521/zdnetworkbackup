<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Icon } from '@iconify/vue'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { CreateUserDialog } from '@/components'
import { logout } from '@/lib/auth'

const router = useRouter()

const showUserModal = ref<boolean>(false)
const user = ref<object | null>(JSON.parse(localStorage.getItem('user') || '{}'))

const logoutUser = async () => {
  await logout()
  await router.push('/login')
}
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button variant="outline">
        <Icon icon="radix-icons:person" class="h-[1.2rem] w-[1.2rem]" />
        {{ user?.user_email || '' }}
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent align="end">
      <DropdownMenuItem @click="showUserModal = true">
        <Icon icon="radix-icons:plus" /> Create New User
      </DropdownMenuItem>
      <DropdownMenuItem @click="() => {}">
        <Icon icon="radix-icons:clock" /> Schedule Backup
      </DropdownMenuItem>
      <Separator />
      <DropdownMenuItem variant="destructive" @click="logoutUser">
        <Icon icon="radix-icons:exit" /> Logout
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
  <CreateUserDialog v-model:show="showUserModal" />
</template>

<style scoped></style>
