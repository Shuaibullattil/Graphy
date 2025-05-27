import * as XLSX from 'xlsx';

export const convertExcelToApiFormat = async (files) => {
  const filesData = await Promise.all(
    Array.from(files).map(async (file) => {
      const arrayBuffer = await file.arrayBuffer();
      const workbook = XLSX.read(arrayBuffer);
      
      return workbook.SheetNames.map(sheetName => {
        const worksheet = workbook.Sheets[sheetName];
        const jsonData = XLSX.utils.sheet_to_json(worksheet);
        
        return {
          fileName: file.name,
          sheetName: sheetName,
          data: jsonData
        };
      });
    })
  );

  return { files: filesData.flat() };
};