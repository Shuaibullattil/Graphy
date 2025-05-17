// DownloadChart.vue
<template>
  <button @click="downloadChart" class="download-button">
    <DownloadIcon class="icon" />
  </button>
</template>

<script>
import { Download as DownloadIcon } from 'lucide-vue-next';

export default {
  name: 'DownloadChart',
  components: { DownloadIcon },
  props: {
    chartRef: {
      type: Object,
      required: true,
    },
    filename: {
      type: String,
      default: 'chart.png',
    },
    size: {
      type: Number,
      default: 1080,
    },
  },
  methods: {
    downloadChart() {
      try {
        if (!this.chartRef) {
          console.warn('No chart reference provided.');
          return;
        }

        // Log the chartRef for debugging
        console.log('Chart reference:', this.chartRef);
        
        // Get the DOM element from the ref
        const chartElement = this.chartRef.$el || this.chartRef;
        console.log('Chart element:', chartElement);
        
        // Find the canvas element within the chart
        const canvas = chartElement.querySelector('canvas');
        if (!canvas) {
          console.warn('Canvas not found inside chart. Trying alternative methods...');
          
          // Try different methods to locate the canvas
          const allCanvases = chartElement.getElementsByTagName('canvas');
          if (allCanvases.length > 0) {
            const canvas = allCanvases[0];
            this.processCanvas(canvas);
            return;
          }
          
          // If we still can't find a canvas
          console.error('No canvas element found in the chart component');
          return;
        }
        
        this.processCanvas(canvas);
      } catch (error) {
        console.error('Error downloading chart:', error);
      }
    },
    
    processCanvas(canvas) {
      try {
        // Create a temporary canvas for resizing if needed
        const tempCanvas = document.createElement('canvas');
        const originalWidth = canvas.width;
        const originalHeight = canvas.height;
        const aspectRatio = originalHeight / originalWidth;
        
        // Set dimension while preserving aspect ratio
        tempCanvas.width = this.size;
        tempCanvas.height = this.size * aspectRatio;
        
        const ctx = tempCanvas.getContext('2d');
        ctx.drawImage(canvas, 0, 0, tempCanvas.width, tempCanvas.height);

        // Create download link
        const link = document.createElement('a');
        link.href = tempCanvas.toDataURL('image/png');
        link.download = this.filename;
        document.body.appendChild(link); // Needed for Firefox
        link.click();
        document.body.removeChild(link);
      } catch (error) {
        console.error('Error processing canvas:', error);
      }
    }
  },
};
</script>

<style scoped>
.download-button {
  margin-top: 1rem;
  padding: 8px 16px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.download-button:hover {
  background-color: #2563eb;
}

.icon {
  width: 18px;
  height: 18px;
}
</style>