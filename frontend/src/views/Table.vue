<template>
  <div class="p-4">
    <h1 class="p-2 bg-pink-700 text-white text-lg font-bold mb-4">This is your table component</h1>
    <table class="min-w-full border border-gray-300">
      <thead class="bg-gray-100">
        <tr>
          <th class="border px-4 py-2 text-left">Name</th>
          <th class="border px-4 py-2 text-left">Email</th>
          <th class="border px-4 py-2 text-left">Filename</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="border px-4 py-2">Shuaib</td>
          <td class="border px-4 py-2">shuaib@example.com</td>
          <td class="border px-4 py-2">report.xlsx</td>
        </tr>
        <!-- You can add more <tr> rows dynamically using v-for later -->
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
    name : "Yourtable"
}

</script>
