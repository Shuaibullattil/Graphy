<template>
  <div v-if="show" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full mx-4 overflow-hidden" @click.stop>
      <div class="p-6">
        <div class="flex items-start gap-4 mb-4">
          <div class="bg-red-100 p-3 rounded-full">
            <AlertTriangle class="h-6 w-6 text-red-600" />
          </div>
          <div class="flex-1">
            <h3 class="text-xl font-semibold text-slate-800 mb-1">Delete Graph</h3>
            <p class="text-slate-500 text-sm">This action cannot be undone</p>
          </div>
        </div>
        
        <p class="text-slate-600 mb-6 leading-relaxed">
          Are you sure you want to permanently delete this graph? All associated data will be lost forever.
        </p>
        
        <div class="flex gap-3">
          <button 
            @click="$emit('cancel')" 
            class="flex-1 px-4 py-3 bg-slate-100 text-slate-700 rounded-xl font-medium 
                   hover:bg-slate-200 transition-colors duration-200"
          >
            Cancel
          </button>
          <button 
            @click="$emit('confirm')" 
            class="flex-1 px-4 py-3 bg-red-500 text-white rounded-xl font-medium 
                   hover:bg-red-600 transition-all duration-200 disabled:opacity-50 
                   disabled:cursor-not-allowed flex items-center justify-center gap-2"
            :disabled="isDeleting"
          >
            <Trash2 v-if="!isDeleting" class="h-4 w-4" />
            <div v-else class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            {{ isDeleting ? 'Deleting...' : 'Delete Graph' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { AlertTriangle, Trash2 } from 'lucide-vue-next'

export default {
  name: 'DeleteModal',
  components: { AlertTriangle, Trash2 },
  props: {
    show: Boolean,
    isDeleting: Boolean,
  },
  emits: ['confirm', 'cancel'],
}
</script>