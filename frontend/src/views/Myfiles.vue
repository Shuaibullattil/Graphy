<template>
    <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-6">
        <!-- Header Section -->
        <div class="max-w-7xl mx-auto mb-8">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">My Files</h1>
                    <p class="text-gray-600">Manage and organize your uploaded files</p>
                </div>
                <div class="flex items-center space-x-4">
                    <div class="bg-white px-4 py-2 rounded-lg shadow-sm border">
                        <span class="text-sm text-gray-500">Total Files:</span>
                        <span class="ml-2 font-semibold text-gray-900">{{ allMyFiles.length }}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="max-w-7xl mx-auto">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div v-for="n in 6" :key="n" class="animate-pulse">
                    <div class="bg-white rounded-xl h-48 shadow-sm border"></div>
                </div>
            </div>
        </div>

        <!-- Files Grid -->
        <div v-else-if="allMyFiles.length > 0" class="max-w-7xl mx-auto">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div v-for="file in allMyFiles" :key="file.file_id" class="group">
                    <!-- Enhanced Card Design -->
                    <div class="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-lg hover:border-violet-300 transition-all duration-300 h-full relative overflow-hidden">
                        <!-- Card Header with Delete Button -->
                        <div class="p-6 pb-4">
                            <div class="flex items-start justify-between mb-3">
                                <div class="flex items-center space-x-3">
                                    <div class="w-10 h-10 bg-gradient-to-br from-violet-500 to-purple-600 rounded-lg flex items-center justify-center">
                                        <FileText class="w-5 h-5 text-white" />
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <h2 class="text-lg font-semibold text-gray-900 truncate">
                                            {{ file.sheetName }}
                                        </h2>
                                    </div>
                                </div>
                                
                                <!-- Delete Button -->
                                <button
                                    @click.stop="confirmDelete(file)"
                                    class="opacity-0 group-hover:opacity-100 transition-opacity duration-200 p-2 hover:bg-red-50 rounded-lg"
                                    title="Delete file"
                                >
                                    <Trash2 class="w-4 h-4 text-red-500 hover:text-red-700" />
                                </button>
                            </div>

                            <!-- File ID -->
                            <div class="flex items-center space-x-2 mb-4">
                                <Hash class="w-4 h-4 text-gray-400" />
                                <span class="text-sm text-gray-500 font-mono">{{ file.file_id }}</span>
                            </div>

                            <!-- Labels -->
                            <div class="mb-4">
                                <div class="flex items-center space-x-2 mb-2">
                                    <Tag class="w-4 h-4 text-gray-400" />
                                    <span class="text-sm font-medium text-gray-700">Labels</span>
                                </div>
                                <div class="flex flex-wrap gap-2">
                                    <span 
                                        v-for="(label, index) in file.labels" 
                                        :key="index"
                                        class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-violet-100 text-violet-800"
                                    >
                                        {{ label }}
                                    </span>
                                    <span 
                                        v-if="file.labels.length === 0"
                                        class="text-xs text-gray-400 italic"
                                    >
                                        No labels
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- Card Footer/Action Area -->
                        <div class="px-6 pb-6">
                            <button
                                @click="openModal(file)"
                                class="w-full bg-gradient-to-r from-violet-500 to-purple-600 hover:from-violet-600 hover:to-purple-700 text-white font-medium py-2.5 px-4 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2"
                            >
                                <Link class="w-4 h-4" />
                                <span>Link to Graph</span>
                            </button>
                        </div>

                        <!-- Hover Overlay -->
                        <div class="absolute inset-0 bg-gradient-to-r from-violet-500/5 to-purple-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Empty State -->
        <div v-else class="max-w-2xl mx-auto text-center py-16">
            <div class="w-24 h-24 mx-auto mb-6 bg-gray-100 rounded-full flex items-center justify-center">
                <Folder class="w-12 h-12 text-gray-400" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">No files found</h3>
            <p class="text-gray-600 mb-6">Get started by uploading your first file</p>
            <button class="bg-violet-500 hover:bg-violet-600 text-white font-medium py-2.5 px-6 rounded-lg transition-colors duration-200">
                Upload File
            </button>
        </div>

        <!-- Modal Component -->
        <LinkFileToGraph 
            v-if="showModal"
            :file-data="selectedFile"
            @close="closeModal"
            @success="handleSuccess"
        />

        <!-- Delete Confirmation Modal -->
        <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div class="bg-white rounded-xl shadow-2xl max-w-md w-full">
                <div class="p-6">
                    <div class="flex items-center space-x-3 mb-4">
                        <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
                            <AlertTriangle class="w-6 h-6 text-red-600" />
                        </div>
                        <div>
                            <h3 class="text-lg font-semibold text-gray-900">Delete File</h3>
                            <p class="text-sm text-gray-600">This action cannot be undone</p>
                        </div>
                    </div>
                    
                    <p class="text-gray-700 mb-6">
                        Are you sure you want to delete "<strong>{{ fileToDelete?.sheetName }}</strong>"?
                    </p>
                    
                    <div class="flex space-x-3">
                        <button
                            @click="cancelDelete"
                            class="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2.5 px-4 rounded-lg transition-colors duration-200"
                            :disabled="deleting"
                        >
                            Cancel
                        </button>
                        <button
                            @click="deleteFile"
                            class="flex-1 bg-red-500 hover:bg-red-600 text-white font-medium py-2.5 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
                            :disabled="deleting"
                        >
                            <Loader2 v-if="deleting" class="w-4 h-4 animate-spin" />
                            <Trash2 v-else class="w-4 h-4" />
                            <span>{{ deleting ? 'Deleting...' : 'Delete' }}</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Success/Error Toast -->
        <div v-if="toast.show" class="fixed top-4 right-4 z-50">
            <div :class="[
                'px-6 py-4 rounded-lg shadow-lg flex items-center space-x-3 transform transition-all duration-300',
                toast.type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
            ]">
                <CheckCircle v-if="toast.type === 'success'" class="w-5 h-5" />
                <XCircle v-else class="w-5 h-5" />
                <span class="font-medium">{{ toast.message }}</span>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import LinkFileToGraph from '../components/LinkFileToGraph.vue'
import {
    FileText,
    Trash2,
    Hash,
    Tag,
    Link,
    Folder,
    AlertTriangle,
    CheckCircle,
    XCircle,
    Loader2
} from 'lucide-vue-next'

export default {
    name: "MYfiles",
    components: {
        LinkFileToGraph,
        FileText,
        Trash2,
        Hash,
        Tag,
        Link,
        Folder,
        AlertTriangle,
        CheckCircle,
        XCircle,
        Loader2
    },
    setup() {
        const allMyFiles = ref([])
        const loading = ref(true)
        const showModal = ref(false)
        const selectedFile = ref(null)
        const showDeleteModal = ref(false)
        const fileToDelete = ref(null)
        const deleting = ref(false)
        const toast = ref({
            show: false,
            type: 'success',
            message: ''
        })
        
        // API call to fetch files
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
                showToast('error', 'Failed to load files')
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
            showToast('success', 'File linked successfully!')
        }

        const confirmDelete = (file) => {
            fileToDelete.value = file
            showDeleteModal.value = true
        }

        const cancelDelete = () => {
            showDeleteModal.value = false
            fileToDelete.value = null
        }

        const deleteFile = async () => {
            if (!fileToDelete.value) return

            deleting.value = true
            
            try {
                const token = sessionStorage.getItem('authToken')
                const baseUrl = 'http://localhost:8000' // You can make this configurable
                
                await axios.delete(`${baseUrl}/file/drop?file_id=${fileToDelete.value.file_id}`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                })

                // Remove the file from the local array
                allMyFiles.value = allMyFiles.value.filter(
                    file => file.file_id !== fileToDelete.value.file_id
                )

                showToast('success', 'File deleted successfully!')
                cancelDelete()

            } catch (error) {
                console.error('Error deleting file:', error)
                showToast('error', 'Failed to delete file')
            } finally {
                deleting.value = false
            }
        }

        const showToast = (type, message) => {
            toast.value = {
                show: true,
                type,
                message
            }

            setTimeout(() => {
                toast.value.show = false
            }, 3000)
        }

        return {
            allMyFiles,
            loading,
            showModal,
            selectedFile,
            showDeleteModal,
            fileToDelete,
            deleting,
            toast,
            openModal,
            closeModal,
            handleSuccess,
            confirmDelete,
            cancelDelete,
            deleteFile
        }
    }
}
</script>

<style scoped>
/* Additional custom styles if needed */
.animate-pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: .5;
    }
}
</style>