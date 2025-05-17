<template>
  <div class="upload-wrapper">
    <label class="upload-label">
      <Upload class="icon" />
      <span>Upload Excel/CSV</span>
      <input type="file" @change="handleFileUpload" accept=".xlsx, .csv" hidden />
    </label>
  </div>
</template>

<script setup>
import * as XLSX from 'xlsx'
import { Upload } from 'lucide-vue-next' // Vue-compatible Lucide icon

const emit = defineEmits(['dataParsed'])

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return

  const reader = new FileReader()

  reader.onload = (e) => {
    try {
      const data = new Uint8Array(e.target.result)
      const workbook = XLSX.read(data, { type: 'array' })
      const sheetName = workbook.SheetNames[0]
      const sheet = workbook.Sheets[sheetName]

      const jsonData = XLSX.utils.sheet_to_json(sheet)
      emit('dataParsed', jsonData)
    } catch (err) {
      console.error('Error parsing file:', err)
    }
  }

  reader.readAsArrayBuffer(file)
}
</script>

<style scoped>
.upload-wrapper {
  display: flex;
  justify-content: center;
  margin: 1rem 0;
}

.upload-label {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #10b981;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-weight: 500;
}

.upload-label:hover {
  background-color: #059669;
}

.icon {
  width: 20px;
  height: 20px;
}
</style>
