<template>
  <div class="flex flex-col items-center">
    <input
      type="file"
      ref="fileInput"
      multiple
      accept=".xlsx,.xls,.csv"
      @change="handleFileUpload"
      class="hidden"
    />
    <button
      @click="triggerFileInput"
      class="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg shadow-md transition-all duration-200"
      :disabled="isLoading"
    >
      <Upload class="w-5 h-5" />
      <span>{{ isLoading ? 'Uploading...' : buttonText }}</span>
      <Loader2 v-if="isLoading" class="w-4 h-4 animate-spin" />
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Upload, Loader2 } from 'lucide-vue-next';
import { convertExcelToApiFormat } from '@/utils/excelConverter';

const props = defineProps({
  buttonText: {
    type: String,
    default: 'Upload Excel Files'
  }
});

const emit = defineEmits(['success', 'error']);
const authToken = sessionStorage.getItem('authToken');
const fileInput = ref(null);
const isLoading = ref(false);

const triggerFileInput = () => fileInput.value.click();

const handleFileUpload = async (event) => {
  const files = event.target.files;
  if (!files.length) return;

  isLoading.value = true;
  
  try {
    const payload = await convertExcelToApiFormat(files);
    const response = await uploadToApi(payload);
    emit('success', response);
  } catch (error) {
    emit('error', error);
  } finally {
    isLoading.value = false;
    event.target.value = '';
  }
};

const uploadToApi = async (payload) => {
  const response = await fetch('http://127.0.0.1:8000/file/upload', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authToken}`
    },
    body: JSON.stringify(payload)
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Upload failed');
  }
  
  return await response.json();
};
</script>