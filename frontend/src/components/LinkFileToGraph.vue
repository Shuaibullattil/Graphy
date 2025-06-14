<template>
    <!-- Modal Overlay -->
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <!-- Modal Header -->
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl font-bold text-gray-800">Link File to Graph</h2>
                <button 
                    @click="$emit('close')"
                    class="text-gray-500 hover:text-gray-700 text-2xl"
                >
                    ×
                </button>
            </div>

            <!-- File Info -->
            <div class="mb-6 p-4 bg-gray-50 rounded-lg">
                <h3 class="text-lg font-semibold mb-2">{{ fileData.sheetName }}</h3>
                <p class="text-sm text-gray-600 mb-2">File ID: {{ fileData.file_id }}</p>
                <div class="flex flex-wrap gap-2">
                    <span 
                        v-for="label in fileData.labels" 
                        :key="label"
                        class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded"
                    >
                        {{ label }}
                    </span>
                </div>
            </div>

            <!-- Simple Form -->
            <form @submit.prevent="handleSubmit">
                <!-- Graph Name Input -->
                <div class="mb-6">
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                        Graph Name
                    </label>
                    <input 
                        v-model="formData.name"
                        type="text" 
                        required
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-violet-500"
                        placeholder="Enter graph name"
                    />
                </div>

                <!-- Labels Selection -->
                <div class="mb-6">
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                        Select Labels
                    </label>
                    <div class="flex flex-wrap gap-2">
                        <label 
                            v-for="label in fileData.labels" 
                            :key="label"
                            class="flex items-center space-x-2 bg-gray-100 p-2 rounded cursor-pointer hover:bg-gray-200"
                        >
                            <input 
                                type="checkbox"
                                :value="label"
                                v-model="formData.labels"
                                class="text-violet-600 focus:ring-violet-500"
                            />
                            <span class="text-sm">{{ label }}</span>
                        </label>
                    </div>
                    <p v-if="formData.labels.length === 0" class="text-red-500 text-sm mt-2">
                        Please select at least one label
                    </p>
                </div>

                <!-- Graph Type Selection -->
                <div class="mb-6">
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                        Select Graph Type
                    </label>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div 
                            v-for="(config, graphId) in graphConfig" 
                            :key="graphId"
                            class="border rounded-lg p-4 cursor-pointer transition-colors"
                            :class="formData.graph_id === graphId ? 'border-violet-500 bg-violet-50' : 'border-gray-300 hover:border-gray-400'"
                            @click="formData.graph_id = graphId"
                        >
                            <input 
                                type="radio"
                                :value="graphId"
                                v-model="formData.graph_id"
                                class="mb-2"
                            />
                            <h4 class="font-semibold">{{ config.title }}</h4>
                            <p class="text-sm text-gray-600">{{ config.component }}</p>
                        </div>
                    </div>
                </div>

                <!-- Graph Preview Component -->
                <div v-if="formData.graph_id && formData.labels.length > 0" class="mb-6">
                    <h3 class="text-lg font-semibold mb-4">Preview</h3>
                    <GraphPreview :previewProps="previewProps" />
                </div>

                <!-- Action Buttons -->
                <div class="flex justify-end space-x-4">
                    <button 
                        type="button"
                        @click="$emit('close')"
                        class="px-4 py-2 text-gray-600 bg-gray-200 rounded hover:bg-gray-300 transition-colors"
                    >
                        Cancel
                    </button>
                    <button 
                        type="submit"
                        :disabled="!isFormValid || loading"
                        class="px-4 py-2 bg-violet-600 text-white rounded hover:bg-violet-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        {{ loading ? 'Linking...' : 'Link Graph' }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import { ref, computed, reactive } from 'vue'
import axios from 'axios'
import GraphPreview from './GraphPreview.vue'

export default {
    name: 'LinkFileToGraph',
    components: {
        GraphPreview
    },
    props: {
        fileData: {
            type: Object,
            required: true
        }
    },
    emits: ['close', 'success'],
    setup(props, { emit }) {
        const loading = ref(false)
        
        const graphConfig = {
            '001': {
                component: 'BarGraph',
                title: 'Bar Chart'
            },
            '002': {
                component: 'PIEChart',
                title: 'Pie Chart'
            },
            '003': {
                component: 'DoughnutGraph',
                title: 'Doughnut Chart'
            }
        }

        const formData = reactive({
            name: '',
            file_id: props.fileData.file_id,
            sheetName: props.fileData.sheetName,
            labels: [],
            graph_id: ''
        })

        // Computed property for preview props
        const previewProps = computed(() => ({
            name: formData.name,
            file_id: formData.file_id,
            sheetName: formData.sheetName,
            labels: formData.labels,
            graph_id: formData.graph_id
        }))

        const isFormValid = computed(() => {
            return formData.name.trim() !== '' && 
                   formData.labels.length > 0 && 
                   formData.graph_id !== ''
        })

        const handleSubmit = async () => {
            if (!isFormValid.value) return

            loading.value = true
            
            try {
                const token = sessionStorage.getItem('authToken')
                const response = await axios.post(
                    'http://localhost:8000/graph/filetograph', 
                    formData,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        }
                    }
                )

                console.log('Graph linked successfully:', response.data)
                emit('success', response.data)
                
            } catch (error) {
                console.error('Error linking graph:', error)
                alert('Error linking graph. Please try again.')
            } finally {
                loading.value = false
            }
        }

        return {
            loading,
            graphConfig,
            formData,
            previewProps,
            isFormValid,
            handleSubmit
        }
    }
}
</script>