<template>
    <div>
        <!-- Files Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <!-- Loop through each file in allMyfiles -->
            <div v-for="file in allMyFiles" :key="file.file_id" class="col-span-1">
                <!-- Card to display file metadata -->
                <div 
                    class="text-left bg-violet-300 p-4 rounded-md h-full cursor-pointer hover:bg-violet-400 transition-colors"
                    @click="openModal(file)"
                >
                    <h2 class="text-xl font-bold mb-2">{{ file.sheetName }}</h2>
                    <p class="text-sm text-gray-700 mb-2">File ID: {{ file.file_id }}</p>
                    <div class="flex flex-wrap gap-2">
                        <!-- Loop through each label in the file -->
                        <span 
                            v-for="(label, index) in file.labels" 
                            :key="index"
                            class="bg-violet-100 text-violet-800 text-xs px-2 py-1 rounded"
                        >
                            {{ label }}
                        </span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal Component -->
        <LinkFileToGraph 
            v-if="showModal"
            :file-data="selectedFile"
            @close="closeModal"
            @success="handleSuccess"
        />
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import LinkFileToGraph from '../components/LinkFileToGraph.vue'

export default {
    name: "MYfiles",
    components: {
        LinkFileToGraph
    },
    setup() {
        const allMyFiles = ref([])
        const loading = ref(true)
        const showModal = ref(false)
        const selectedFile = ref(null)
        
        // API call
        onMounted(async () => {
            try {
                const token = sessionStorage.getItem('authToken')
                const response = await axios.get('http://localhost:8000/file/about', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                })

                allMyFiles.value = response.data.files

            } catch (error) {
                console.error('Error fetching file data:', error)
            } finally {
                loading.value = false
            }
        })

        const openModal = (file) => {
            selectedFile.value = file
            showModal.value = true
        }

        const closeModal = () => {
            showModal.value = false
            selectedFile.value = null
        }

        const handleSuccess = () => {
            closeModal()
            // You can add additional success handling here
            // like showing a success message or refreshing data
        }

        return {
            allMyFiles,
            loading,
            showModal,
            selectedFile,
            openModal,
            closeModal,
            handleSuccess
        }
    }
}
</script>