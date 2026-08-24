import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// React의 최신 JSX 변환 방식을 Vite에 연결합니다.
// 이 설정이 없으면 JSX 파일에서 React를 찾지 못해 화면이 비어 보일 수 있습니다.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:5001",
        changeOrigin: true,
      },
    },
  },
});
