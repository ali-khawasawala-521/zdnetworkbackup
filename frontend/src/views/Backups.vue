<script lang="ts" setup>
import type { Backup } from '@/types/backup'

import { ref, onMounted } from 'vue'
import { BackupTable } from '@/components'
import { getBackupList } from '@/lib/backup'

const backups = ref<Backup[]>([])

const handleLoadBackups = async () => {
  backups.value = await getBackupList()
}

onMounted(handleLoadBackups)
</script>

<template>
  <div class="max-w-[1920px] p-4 mx-auto">
    <BackupTable :backups="backups" @refresh:devices="handleLoadBackups" />
  </div>
</template>

<style></style>
