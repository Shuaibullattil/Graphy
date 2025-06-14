<template>
  <div>
    <!-- File Icons Section -->
    <div class="p-4 bg-gray-50 border-b">
      <h2 class="text-xl font-bold mb-4 text-gray-800">Your Files</h2>
      <MultipleFileUploadButton />
      
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-pink-700"></div>
        <span class="ml-2 text-gray-600">Loading files...</span>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
        <div class="font-semibold">Error loading files:</div>
        <div class="text-sm mt-1">{{ error }}</div>
        <button 
          @click="fetchFileData" 
          class="mt-2 px-3 py-1 bg-red-100 hover:bg-red-200 rounded text-sm transition-colors"
        >
          Retry
        </button>
      </div>
      
      <!-- Files Display -->
      <div v-else-if="fileData.length > 0" class="flex flex-wrap gap-4">
        <div 
          v-for="(file, index) in fileData" 
          :key="index"
          @click="selectFile(index)"
          :class="[
            'cursor-pointer p-4 border-2 rounded-lg transition-all duration-200 hover:shadow-lg min-w-[160px] text-center',
            selectedFileIndex === index 
              ? 'border-pink-700 bg-pink-50 shadow-md' 
              : 'border-gray-300 bg-white hover:border-gray-400'
          ]"
        >
          <!-- Excel File Icon -->
          <div class="mb-2">
            <svg class="w-12 h-12 mx-auto text-green-600" fill="currentColor" viewBox="0 0 24 24">
              <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
              <path d="M12.5,11L14.5,14H13L11.75,12.5L10.5,14H9L11,11L9,8H10.5L11.75,9.5L13,8H14.5L12.5,11Z"/>
            </svg>
          </div>
          <!-- Sheet Name (Bigger) -->
          <div class="text-lg font-bold text-gray-800 mb-1">
            {{ file.sheetName }}
          </div>
          <!-- File Name (Smaller) -->
          <div class="text-sm text-gray-600">
            {{ file.fileName }}
          </div>
          <!-- Upload Date -->
          <div class="text-xs text-gray-500 mt-1">
            {{ formatDate(file.uploaded_at) }}
          </div>
        </div>
      </div>
      
      <!-- No Files State -->
      <div v-else class="text-gray-500 text-center py-8">
        No files found. Upload some files to get started.
      </div>
    </div>

    <!-- Table Section -->
    <div class="p-4">
      <h1 class="p-2 bg-pink-700 text-white text-lg font-bold mb-4">
        {{ selectedFile ? `Data from ${selectedFile.sheetName}` : 'Select a file to view data' }}
      </h1>
      
      <div v-if="selectedFile && selectedFile.data.length > 0">
        <div class="mb-2 text-sm text-gray-600">
          Showing {{ selectedFile.data.length }} records from {{ selectedFile.fileName }}
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full border border-gray-300 bg-white shadow-sm">
            <thead class="bg-gray-100">
              <tr>
                <th 
                  v-for="header in tableHeaders" 
                  :key="header"
                  class="border px-4 py-2 text-left font-semibold text-gray-700"
                >
                  {{ header }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="(row, index) in selectedFile.data" 
                :key="index"
                :class="index % 2 === 0 ? 'bg-white' : 'bg-gray-50'"
                class="hover:bg-blue-50 transition-colors duration-150"
              >
                <td 
                  v-for="header in tableHeaders" 
                  :key="header"
                  class="border px-4 py-2 text-gray-800"
                >
                  {{ formatCellValue(row[header], header) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <div v-else-if="selectedFile && selectedFile.data.length === 0" class="text-gray-500 text-center py-8">
        No data available in this file.
      </div>
      
      <div v-else class="text-gray-500 text-center py-8">
        Click on a file above to view its contents.
      </div>
    </div>
  </div>
</template>

<script>
import MultipleFileUploadButton from '@/components/MultipleFileUploadButton.vue';
export default {
  name: "YourTable",
  components:{
    MultipleFileUploadButton
  },
  data() {
    return {
      selectedFileIndex: 0,
      fileData: [],
      loading: true,
      error: null
    }
  },
  async mounted() {
    await this.fetchFileData();
  },
  computed: {
    selectedFile() {
      return this.fileData && this.fileData.length > 0 ? this.fileData[this.selectedFileIndex] || null : null;
    },
    tableHeaders() {
      if (this.selectedFile && this.selectedFile.data.length > 0) {
        return Object.keys(this.selectedFile.data[0]);
      }
      return [];
    }
  },
  methods: {
    async fetchFileData() {
      this.loading = true;
      this.error = null;
      
      try {
        // Get JWT token from sessionStorage
        const authToken = sessionStorage.getItem('authToken');
        
        if (!authToken) {
          throw new Error('Authentication token not found. Please login again.');
        }
        
        const response = await fetch('http://127.0.0.1:8000/file/my', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${authToken}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (!response.ok) {
          if (response.status === 401) {
            throw new Error('Authentication failed. Please login again.');
          }
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        this.fileData = data;
        
        // Set default selection to first file if available
        if (this.fileData.length > 0) {
          this.selectedFileIndex = 0;
        }
        
      } catch (err) {
        this.error = err.message || 'Failed to fetch file data';
        console.error('Error fetching file data:', err);
      } finally {
        this.loading = false;
      }
    },
    selectFile(index) {
      this.selectedFileIndex = index;
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },
    formatCellValue(value, header) {
      // Format specific data types
      if (header === 'Date' && value) {
        return new Date(value).toLocaleDateString();
      }
      if ((header === 'Price' || header === 'Total' || header === 'Revenue') && typeof value === 'number') {
        return `$${value.toLocaleString()}`;
      }
      if (typeof value === 'number') {
        return value.toLocaleString();
      }
      return value || '';
    }
  }
}
</script>

<style scoped>
/* Add any additional custom styles here if needed */
.hover\:shadow-lg:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}
</style>