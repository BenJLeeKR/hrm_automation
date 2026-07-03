/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  // 브라우저가 백엔드 주소(NEXT_PUBLIC_API_BASE_URL, 빌드 시점에 고정됨)를 직접 몰라도
  // 되도록, /api/v1/* 요청을 Next.js 서버가 Docker 내부망의 api 컨테이너로 대신 전달한다.
  // 이렇게 하면 LAN IP 직접 접속·SSH 터널(웹 포트 3030만 열면 됨)·localhost 등 접속
  // 방식과 무관하게 항상 동작한다 — NEXT_PUBLIC_API_BASE_URL을 비워두면(.env에서 빈 값)
  // 프론트엔드 코드(lib/api.ts, lib/auth.ts)가 상대 경로로 호출해 이 프록시를 타게 된다.
  // `api:8000`은 docker-compose.yml의 서비스명·내부 포트로, Docker 내부 DNS로만
  // 해석되는 값이라 민감정보가 아니다.
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: 'http://api:8000/api/v1/:path*',
      },
    ]
  },
}

export default nextConfig
