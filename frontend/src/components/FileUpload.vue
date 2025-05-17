<template>
  <div>
    <input type="file" @change="handleFileUpload" accept=".xlsx, .csv" />
  </div>
</template>

<script setup>
import * as XLSX from 'xlsx'

const emit = defineEmits(['dataParsed'])

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (e) => {
    const data = new Uint8Array(e.target.result)
    const workbook = XLSX.read(data, { type: 'array' })
    const sheetName = workbook.SheetNames[0]
    const sheet = workbook.Sheets[sheetName]

    const jsonData = XLSX.utils.sheet_to_json(sheet)
    emit('dataParsed', jsonData)
  }
  reader.readAsArrayBuffer(file)
}
</script>
