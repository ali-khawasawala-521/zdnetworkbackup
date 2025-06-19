<script setup lang="ts">
import type { Backup } from '@/types/backup'

import { ref } from 'vue'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { AlertDialog, BackupDialog } from '@/components'
import { get_device_type } from '@/lib/device'
import { getBackup, deleteBackup, downloadBackup } from '@/lib/backup'
import { formatLocaleDate } from '@/lib/helper'

const { backups = [] } = defineProps<{ backups: Backup[] }>()

const emit = defineEmits<{
  (e: 'refresh:devices'): void
}>()

const alertModal = ref<boolean>(false)
const showBackupModal = ref<boolean>(false)
const backup = ref<Backup | null>(null)
const selectedBackup = ref<Backup | null>(null)

const handleShowBackup = async (bck: Backup) => {
  try {
    backup.value = await getBackup(bck.id)
    showBackupModal.value = true
  } catch (error) {
    console.error(error)
  }
}

const handleDownloadBackup = async (backup: Backup) => {
  await downloadBackup(backup)
}

const handleDeleteBackupModal = (backup: Backup) => {
  selectedBackup.value = backup
  alertModal.value = true
}

const handleDeleteBackup = async (backup: Backup) => {
  await deleteBackup(backup.id)
  await handleLoadBackups()
  selectedBackup.value = null
}

const handleLoadBackups = async () => {
  emit('refresh:devices')
}
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle>Backups</CardTitle>
    </CardHeader>
    <CardContent>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>Device Type</TableHead>
            <TableHead>IP Address</TableHead>
            <TableHead>Hostname</TableHead>
            <TableHead>Created At</TableHead>
            <TableHead class="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow v-for="backup in backups" :key="backup.id">
            <TableCell>{{ backup.id }}</TableCell>
            <TableCell>{{ get_device_type(backup.device_type) }}</TableCell>
            <TableCell>{{ backup.ip_address }}</TableCell>
            <TableCell>{{ backup.hostname }}</TableCell>
            <TableCell>{{ formatLocaleDate(backup.created_at) }}</TableCell>
            <TableCell class="text-right space-x-2">
              <Button size="sm" @click="handleShowBackup(backup)">Show Backup</Button>
              <Button size="sm" @click="handleDownloadBackup(backup)">Download Backup</Button>
              <Button size="sm" variant="destructive" @click="handleDeleteBackupModal(backup)"
                >Delete Backup</Button
              >
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </CardContent>
  </Card>
  <AlertDialog
    v-model:open="alertModal"
    title="Are you sure?"
    :description="`It will remove your backup for ${selectedBackup?.hostname} created at ${formatLocaleDate(selectedBackup?.created_at)}. This action cannot be undone.`"
    @on:ok="handleDeleteBackup(selectedBackup as Backup)"
  />
  <BackupDialog v-model:show="showBackupModal" :backup="backup" />
</template>
