// HRM 자동화 시스템 — 목(Mock) 데이터
// 실제 백엔드 연동 전 프로토타입용. 향후 FastAPI /api/v1/* 로 대체.

import type {
  Assignment,
  AuditLog,
  AvailabilityRow,
  Department,
  Employee,
  JobType,
  Position,
  Project,
  RecommendationRow,
  Skill,
  SystemUser,
} from './types'

export const departments: Department[] = [
  { code: 'DELIVERY', name: '딜리버리' },
  { code: 'SALES_PARTNER', name: '세일즈파트너' },
  { code: 'SALES', name: '영업' },
]

export const positions: Position[] = [
  { code: 'INTERN', name: '인턴', order: 10 },
  { code: 'SAWON', name: '사원', order: 20 },
  { code: 'DAERI', name: '대리', order: 30 },
  { code: 'CHAJANG', name: '차장', order: 40 },
  { code: 'BUJANG', name: '부장', order: 50 },
  { code: 'ISA', name: '이사', order: 60 },
  { code: 'SANGMUBO', name: '상무보', order: 70 },
  { code: 'SANGMU', name: '상무', order: 80 },
  { code: 'JUNMU', name: '전무', order: 90 },
  { code: 'BUDAEPYO', name: '부대표', order: 100 },
]

export const jobTypes: JobType[] = [
  { code: 'ARCHITECT', name: '아키텍트(AA)', group: 'TECHNICAL', desc: '시스템 및 애플리케이션 아키텍처 설계', useYn: true },
  { code: 'TECH_LEAD', name: '기술아키텍트(TA)', group: 'TECHNICAL', desc: '기술 아키텍처 및 인프라 설계', useYn: true },
  { code: 'BA', name: '비즈니스 애널리스트(BA)', group: 'ANALYSIS', desc: '업무 요건 분석 및 요구사항 정의', useYn: true },
  { code: 'DBA', name: 'DBA', group: 'TECHNICAL', desc: '데이터베이스 관리', useYn: true },
  { code: 'PM', name: '프로젝트 매니저(PM)', group: 'MANAGEMENT', desc: '프로젝트 관리', useYn: true },
  { code: 'CONSULTANT', name: '컨설턴트', group: 'MANAGEMENT', desc: '업무 및 IT 컨설팅', useYn: true },
  { code: 'PMO', name: '사업관리', group: 'MANAGEMENT', desc: '사업 관리 및 원가 분석', useYn: true },
  { code: 'DEVELOPER', name: '개발자', group: 'TECHNICAL', desc: '소프트웨어 개발', useYn: true },
  { code: 'QA', name: 'QA 엔지니어', group: 'TECHNICAL', desc: '품질 보증 및 테스트', useYn: true },
  { code: 'DEVOPS', name: 'DevOps/인프라', group: 'TECHNICAL', desc: '인프라, 배포, 운영 자동화', useYn: true },
  { code: 'DESIGNER', name: 'UI/UX 디자이너', group: 'TECHNICAL', desc: '사용자 경험 및 화면 설계', useYn: true },
]

export const skills: Skill[] = [
  { id: 'SK-001', group: 'BACKEND', name: 'Java', userCount: 28, useYn: true },
  { id: 'SK-002', group: 'BACKEND', name: 'Spring', userCount: 25, useYn: true },
  { id: 'SK-003', group: 'BACKEND', name: 'Node.js', userCount: 14, useYn: true },
  { id: 'SK-004', group: 'FRONTEND', name: 'React', userCount: 18, useYn: true },
  { id: 'SK-005', group: 'FRONTEND', name: 'Vue', userCount: 9, useYn: true },
  { id: 'SK-006', group: 'FRONTEND', name: 'TypeScript', userCount: 16, useYn: true },
  { id: 'SK-007', group: 'DB', name: 'Oracle', userCount: 20, useYn: true },
  { id: 'SK-008', group: 'DB', name: 'PostgreSQL', userCount: 12, useYn: true },
  { id: 'SK-009', group: 'DB', name: 'MySQL', userCount: 15, useYn: true },
  { id: 'SK-010', group: 'CLOUD', name: 'AWS', userCount: 11, useYn: true },
  { id: 'SK-011', group: 'CLOUD', name: 'Azure', userCount: 6, useYn: true },
  { id: 'SK-012', group: 'DEVOPS', name: 'Kubernetes', userCount: 7, useYn: true },
  { id: 'SK-013', group: 'DEVOPS', name: 'Jenkins', userCount: 8, useYn: true },
  { id: 'SK-014', group: 'DESIGN', name: 'Figma', userCount: 5, useYn: true },
  { id: 'SK-015', group: 'BUSINESS', name: '전략기획', userCount: 4, useYn: true },
  { id: 'SK-016', group: 'BUSINESS', name: 'BPR', userCount: 3, useYn: true },
  { id: 'SK-017', group: 'BUSINESS', name: '계약관리', userCount: 3, useYn: true },
  { id: 'SK-018', group: 'BACKEND', name: 'EJB', userCount: 0, useYn: false },
]

function trail(items: [string, string, string][]) {
  return items.map(([at, user, message]) => ({ at, user, message }))
}

export const employees: Employee[] = [
  {
    id: 'BW-001',
    empNo: 'BW-001',
    name: '홍길동',
    team: 'DELIVERY',
    position: 'CHAJANG',
    roles: ['PM', 'AA'],
    allocation: 0,
    availableDate: '즉시',
    status: 'ACTIVE',
    email: 'hong@bwware.co.kr',
    phone: '010-1234-5678',
    hireDate: '2018-03-02',
    skills: [
      { skillName: 'Java', group: 'BACKEND', level: 5, years: 8, lastUsed: '2026-07-01' },
      { skillName: 'Spring', group: 'BACKEND', level: 4, years: 7.5, lastUsed: '2026-07-01' },
      { skillName: 'PostgreSQL', group: 'DB', level: 3, years: 3, lastUsed: '2026-06-30' },
    ],
    assignments: [],
    history: trail([
      ['2026-07-01 10:23', 'admin', '직무 변경: DEVELOPER → ARCHITECT'],
      ['2026-06-15 09:10', 'hr_mgr', '기술 숙련도 수정: Spring 3→4'],
      ['2025-12-31 18:00', 'system', 'X프로젝트 투입 종료 처리'],
    ]),
  },
  {
    id: 'BW-002',
    empNo: 'BW-002',
    name: '김철수',
    team: 'DELIVERY',
    position: 'DAERI',
    roles: ['TA'],
    allocation: 100,
    availableDate: '2026-10-01',
    status: 'ACTIVE',
    email: 'kimcs@bwware.co.kr',
    phone: '010-2345-6789',
    hireDate: '2020-01-06',
    skills: [
      { skillName: 'React', group: 'FRONTEND', level: 4, years: 5, lastUsed: '2026-07-01' },
      { skillName: 'Node.js', group: 'BACKEND', level: 4, years: 4.5, lastUsed: '2026-07-01' },
      { skillName: 'AWS', group: 'CLOUD', level: 3, years: 3, lastUsed: '2026-06-20' },
    ],
    assignments: [
      { projectName: 'A사 차세대 STO', role: 'Frontend Lead', allocation: 100, startDate: '2026-04-01', endDate: '2026-09-30', status: 'ACTIVE', type: 'RUNNING' },
    ],
    history: trail([
      ['2026-04-01 09:00', 'pm_lee', 'A사 차세대 STO 투입 등록'],
    ]),
  },
  {
    id: 'BW-003',
    empNo: 'BW-003',
    name: '이영희',
    team: 'DELIVERY',
    position: 'SAWON',
    roles: ['BA'],
    allocation: 160,
    availableDate: '2026-12-01',
    status: 'ACTIVE',
    email: 'leeyh@bwware.co.kr',
    phone: '010-3456-7890',
    hireDate: '2023-07-03',
    skills: [
      { skillName: 'Figma', group: 'DESIGN', level: 4, years: 3, lastUsed: '2026-07-01' },
      { skillName: 'MySQL', group: 'DB', level: 3, years: 2, lastUsed: '2026-06-15' },
    ],
    assignments: [
      { projectName: 'B사 그룹웨어 고도화', role: '업무분석', allocation: 100, startDate: '2026-05-01', endDate: '2026-11-30', status: 'ACTIVE', type: 'RUNNING' },
      { projectName: 'C사 포털 재구축', role: '요건정의', allocation: 60, startDate: '2026-08-01', endDate: '2026-12-31', status: 'PLANNED', type: 'COMMITTED' },
    ],
    history: trail([
      ['2026-07-01 14:12', 'pm_park', 'C사 포털 재구축 투입준비 등록'],
    ]),
  },
  {
    id: 'BW-004',
    empNo: 'BW-004',
    name: '박민준',
    team: 'DELIVERY',
    position: 'DAERI',
    roles: ['DBA'],
    allocation: 80,
    availableDate: '2027-01-01',
    status: 'ACTIVE',
    email: 'parkmj@bwware.co.kr',
    phone: '010-4567-8901',
    hireDate: '2019-09-16',
    skills: [
      { skillName: 'Oracle', group: 'DB', level: 5, years: 6, lastUsed: '2026-07-01' },
      { skillName: 'PostgreSQL', group: 'DB', level: 4, years: 3.5, lastUsed: '2026-06-30' },
    ],
    assignments: [
      { projectName: 'A사 차세대 STO', role: 'DB 설계', allocation: 80, startDate: '2026-04-01', endDate: '2026-12-31', status: 'ACTIVE', type: 'RUNNING' },
    ],
    history: trail([
      ['2026-04-01 09:05', 'pm_lee', 'A사 차세대 STO 투입 등록'],
    ]),
  },
  {
    id: 'BW-005',
    empNo: 'BW-005',
    name: '최수연',
    team: 'SALES_PARTNER',
    position: 'BUJANG',
    roles: ['컨설턴트'],
    allocation: 80,
    availableDate: '2027-03-01',
    status: 'ACTIVE',
    email: 'choisy@bwware.co.kr',
    phone: '010-5678-9012',
    hireDate: '2015-02-02',
    skills: [
      { skillName: '전략기획', group: 'BUSINESS', level: 5, years: 10, lastUsed: '2026-07-01' },
      { skillName: 'BPR', group: 'BUSINESS', level: 4, years: 8, lastUsed: '2026-06-01' },
    ],
    assignments: [
      { projectName: 'D사 디지털 전환 컨설팅', role: '수석 컨설턴트', allocation: 80, startDate: '2026-03-01', endDate: '2027-02-28', status: 'ACTIVE', type: 'RUNNING' },
    ],
    history: trail([
      ['2026-03-01 09:00', 'hr_mgr', 'D사 디지털 전환 컨설팅 투입 등록'],
    ]),
  },
  {
    id: 'BW-006',
    empNo: 'BW-006',
    name: '정재원',
    team: 'SALES',
    position: 'CHAJANG',
    roles: ['사업관리'],
    allocation: 80,
    availableDate: '2027-04-01',
    status: 'ACTIVE',
    email: 'jungjw@bwware.co.kr',
    phone: '010-6789-0123',
    hireDate: '2017-11-01',
    skills: [
      { skillName: '계약관리', group: 'BUSINESS', level: 4, years: 7, lastUsed: '2026-07-01' },
    ],
    assignments: [
      { projectName: 'E사 유지보수 사업', role: '사업관리', allocation: 80, startDate: '2026-01-01', endDate: '2026-12-31', status: 'ACTIVE', type: 'RUNNING' },
    ],
    history: trail([
      ['2026-01-01 09:00', 'admin', 'E사 유지보수 사업 투입 등록'],
    ]),
  },
  {
    id: 'BW-007',
    empNo: 'BW-007',
    name: '강하늘',
    team: 'DELIVERY',
    position: 'SAWON',
    roles: ['DEVELOPER'],
    allocation: 0,
    availableDate: '즉시',
    status: 'ACTIVE',
    email: 'kanghn@bwware.co.kr',
    phone: '010-7890-1234',
    hireDate: '2024-01-02',
    skills: [
      { skillName: 'Java', group: 'BACKEND', level: 3, years: 2, lastUsed: '2026-05-30' },
      { skillName: 'Spring', group: 'BACKEND', level: 3, years: 2, lastUsed: '2026-05-30' },
      { skillName: 'TypeScript', group: 'FRONTEND', level: 2, years: 1, lastUsed: '2026-04-10' },
    ],
    assignments: [],
    history: trail([
      ['2026-05-31 18:00', 'system', 'F사 SI 프로젝트 종료'],
    ]),
  },
  {
    id: 'BW-008',
    empNo: 'BW-008',
    name: '윤서진',
    team: 'DELIVERY',
    position: 'DAERI',
    roles: ['DEVELOPER', 'DEVOPS'],
    allocation: 50,
    availableDate: '2026-09-01',
    status: 'ACTIVE',
    email: 'yoonsj@bwware.co.kr',
    phone: '010-8901-2345',
    hireDate: '2021-06-14',
    skills: [
      { skillName: 'Kubernetes', group: 'DEVOPS', level: 4, years: 3, lastUsed: '2026-07-01' },
      { skillName: 'Jenkins', group: 'DEVOPS', level: 4, years: 3.5, lastUsed: '2026-07-01' },
      { skillName: 'AWS', group: 'CLOUD', level: 4, years: 4, lastUsed: '2026-07-01' },
    ],
    assignments: [
      { projectName: 'B사 그룹웨어 고도화', role: '인프라', allocation: 50, startDate: '2026-05-01', endDate: '2026-08-31', status: 'ACTIVE', type: 'RUNNING' },
    ],
    history: trail([
      ['2026-05-01 09:00', 'pm_park', 'B사 그룹웨어 고도화 투입 등록'],
    ]),
  },
  {
    id: 'BW-009',
    empNo: 'BW-009',
    name: '임도현',
    team: 'DELIVERY',
    position: 'CHAJANG',
    roles: ['AA', 'TA'],
    allocation: 100,
    availableDate: '2026-08-31',
    status: 'ACTIVE',
    email: 'limdh@bwware.co.kr',
    phone: '010-9012-3456',
    hireDate: '2016-08-22',
    skills: [
      { skillName: 'Java', group: 'BACKEND', level: 5, years: 9, lastUsed: '2026-07-01' },
      { skillName: 'AWS', group: 'CLOUD', level: 4, years: 5, lastUsed: '2026-07-01' },
      { skillName: 'PostgreSQL', group: 'DB', level: 4, years: 5, lastUsed: '2026-07-01' },
    ],
    assignments: [
      { projectName: 'G사 클라우드 전환', role: '아키텍트', allocation: 100, startDate: '2026-02-01', endDate: '2026-08-31', status: 'ACTIVE', type: 'RUNNING' },
    ],
    history: trail([
      ['2026-02-01 09:00', 'pm_lee', 'G사 클라우드 전환 투입 등록'],
    ]),
  },
  {
    id: 'BW-010',
    empNo: 'BW-010',
    name: '한지민',
    team: 'DELIVERY',
    position: 'SAWON',
    roles: ['DESIGNER'],
    allocation: 40,
    availableDate: '2026-09-15',
    status: 'ACTIVE',
    email: 'hanjm@bwware.co.kr',
    phone: '010-0123-4567',
    hireDate: '2023-03-02',
    skills: [
      { skillName: 'Figma', group: 'DESIGN', level: 5, years: 4, lastUsed: '2026-07-01' },
      { skillName: 'TypeScript', group: 'FRONTEND', level: 2, years: 1.5, lastUsed: '2026-05-01' },
    ],
    assignments: [
      { projectName: 'C사 포털 재구축', role: 'UI 디자인', allocation: 40, startDate: '2026-06-01', endDate: '2026-09-14', status: 'ACTIVE', type: 'RUNNING' },
    ],
    history: trail([
      ['2026-06-01 09:00', 'pm_park', 'C사 포털 재구축 투입 등록'],
    ]),
  },
  {
    id: 'BW-011',
    empNo: 'BW-011',
    name: '오세훈',
    team: 'DELIVERY',
    position: 'BUJANG',
    roles: ['PM'],
    allocation: 100,
    availableDate: '2026-11-30',
    status: 'ACTIVE',
    email: 'ohsh@bwware.co.kr',
    phone: '010-1112-2233',
    hireDate: '2013-05-13',
    skills: [
      { skillName: 'Java', group: 'BACKEND', level: 4, years: 12, lastUsed: '2025-12-01' },
      { skillName: 'Oracle', group: 'DB', level: 4, years: 10, lastUsed: '2025-12-01' },
    ],
    assignments: [
      { projectName: 'A사 차세대 STO', role: 'PM', allocation: 100, startDate: '2026-04-01', endDate: '2026-11-30', status: 'ACTIVE', type: 'RUNNING' },
    ],
    history: trail([
      ['2026-04-01 08:55', 'admin', 'A사 차세대 STO PM 지정'],
    ]),
  },
  {
    id: 'BW-012',
    empNo: 'BW-012',
    name: '서지우',
    team: 'DELIVERY',
    position: 'DAERI',
    roles: ['QA'],
    allocation: 0,
    availableDate: '즉시',
    status: 'ACTIVE',
    email: 'seojw@bwware.co.kr',
    phone: '010-2223-3344',
    hireDate: '2021-02-01',
    skills: [
      { skillName: 'Java', group: 'BACKEND', level: 3, years: 3, lastUsed: '2026-06-01' },
      { skillName: 'MySQL', group: 'DB', level: 3, years: 3, lastUsed: '2026-06-01' },
    ],
    assignments: [],
    history: trail([
      ['2026-05-31 18:00', 'system', 'F사 SI 프로젝트 QA 종료'],
    ]),
  },
  {
    id: 'BW-013',
    empNo: 'BW-013',
    name: '문가영',
    team: 'SALES_PARTNER',
    position: 'CHAJANG',
    roles: ['컨설턴트', 'BA'],
    allocation: 50,
    availableDate: '2026-10-15',
    status: 'ACTIVE',
    email: 'moongy@bwware.co.kr',
    phone: '010-3334-4455',
    hireDate: '2018-10-08',
    skills: [
      { skillName: 'BPR', group: 'BUSINESS', level: 4, years: 6, lastUsed: '2026-07-01' },
      { skillName: '전략기획', group: 'BUSINESS', level: 4, years: 6, lastUsed: '2026-07-01' },
    ],
    assignments: [
      { projectName: 'D사 디지털 전환 컨설팅', role: '컨설턴트', allocation: 50, startDate: '2026-03-01', endDate: '2026-10-14', status: 'ACTIVE', type: 'RUNNING' },
    ],
    history: trail([
      ['2026-03-01 09:10', 'hr_mgr', 'D사 디지털 전환 컨설팅 투입 등록'],
    ]),
  },
  {
    id: 'BW-014',
    empNo: 'BW-014',
    name: '배준호',
    team: 'DELIVERY',
    position: 'SAWON',
    roles: ['DEVELOPER'],
    allocation: 0,
    availableDate: '즉시',
    status: 'LEAVE',
    email: 'baejh@bwware.co.kr',
    phone: '010-4445-5566',
    hireDate: '2022-04-11',
    skills: [
      { skillName: 'React', group: 'FRONTEND', level: 3, years: 2.5, lastUsed: '2026-03-01' },
      { skillName: 'Node.js', group: 'BACKEND', level: 3, years: 2, lastUsed: '2026-03-01' },
    ],
    assignments: [],
    history: trail([
      ['2026-04-01 09:00', 'hr_mgr', '휴직 처리 (육아휴직)'],
    ]),
  },
]

export const projects: Project[] = [
  {
    id: 'PJT-001',
    code: 'PJT-2026-001',
    name: 'A사 차세대 STO',
    client: 'A증권',
    status: 'RUNNING',
    startDate: '2026-04-01',
    endDate: '2026-11-30',
    memberCount: 4,
    desc: '차세대 증권 트레이딩 시스템 구축 프로젝트',
    members: [
      { empNo: 'BW-011', name: '오세훈', role: 'PM', allocation: 100, type: 'RUNNING', startDate: '2026-04-01', endDate: '2026-11-30' },
      { empNo: 'BW-002', name: '김철수', role: 'Frontend Lead', allocation: 100, type: 'RUNNING', startDate: '2026-04-01', endDate: '2026-09-30' },
      { empNo: 'BW-004', name: '박민준', role: 'DB 설계', allocation: 80, type: 'RUNNING', startDate: '2026-04-01', endDate: '2026-12-31' },
      { empNo: 'BW-009', name: '임도현', role: '아키텍트', allocation: 100, type: 'COMMITTED', startDate: '2026-09-01', endDate: '2026-12-31' },
    ],
    history: trail([
      ['2026-04-01 09:00', 'admin', '프로젝트 등록 및 착수'],
      ['2026-06-15 11:00', 'pm_ohsh', '투입 인력 1명 추가'],
    ]),
  },
  {
    id: 'PJT-002',
    code: 'PJT-2026-002',
    name: 'B사 그룹웨어 고도화',
    client: 'B물산',
    status: 'RUNNING',
    startDate: '2026-05-01',
    endDate: '2026-11-30',
    memberCount: 2,
    desc: '사내 그룹웨어 UI/UX 개선 및 인프라 현대화',
    members: [
      { empNo: 'BW-003', name: '이영희', role: '업무분석', allocation: 100, type: 'RUNNING', startDate: '2026-05-01', endDate: '2026-11-30' },
      { empNo: 'BW-008', name: '윤서진', role: '인프라', allocation: 50, type: 'RUNNING', startDate: '2026-05-01', endDate: '2026-08-31' },
    ],
    history: trail([
      ['2026-05-01 09:00', 'pm_park', '프로젝트 등록 및 착수'],
    ]),
  },
  {
    id: 'PJT-003',
    code: 'PJT-2026-003',
    name: 'C사 포털 재구축',
    client: 'C공사',
    status: 'RUNNING',
    startDate: '2026-06-01',
    endDate: '2026-12-31',
    memberCount: 2,
    desc: '대국민 포털 사이트 전면 재구축',
    members: [
      { empNo: 'BW-010', name: '한지민', role: 'UI 디자인', allocation: 40, type: 'RUNNING', startDate: '2026-06-01', endDate: '2026-09-14' },
      { empNo: 'BW-003', name: '이영희', role: '요건정의', allocation: 60, type: 'COMMITTED', startDate: '2026-08-01', endDate: '2026-12-31' },
    ],
    history: trail([
      ['2026-05-20 15:00', 'pm_park', '프로젝트 등록'],
    ]),
  },
  {
    id: 'PJT-004',
    code: 'PJT-2026-004',
    name: 'D사 디지털 전환 컨설팅',
    client: 'D그룹',
    status: 'RUNNING',
    startDate: '2026-03-01',
    endDate: '2027-02-28',
    memberCount: 2,
    desc: '전사 디지털 전환 전략 수립 및 로드맵 컨설팅',
    members: [
      { empNo: 'BW-005', name: '최수연', role: '수석 컨설턴트', allocation: 80, type: 'RUNNING', startDate: '2026-03-01', endDate: '2027-02-28' },
      { empNo: 'BW-013', name: '문가영', role: '컨설턴트', allocation: 50, type: 'RUNNING', startDate: '2026-03-01', endDate: '2026-10-14' },
    ],
    history: trail([
      ['2026-03-01 09:00', 'hr_mgr', '프로젝트 등록 및 착수'],
    ]),
  },
  {
    id: 'PJT-005',
    code: 'PJT-2026-005',
    name: 'E사 유지보수 사업',
    client: 'E공단',
    status: 'RUNNING',
    startDate: '2026-01-01',
    endDate: '2026-12-31',
    memberCount: 1,
    desc: '연간 시스템 유지보수 및 운영 사업',
    members: [
      { empNo: 'BW-006', name: '정재원', role: '사업관리', allocation: 80, type: 'RUNNING', startDate: '2026-01-01', endDate: '2026-12-31' },
    ],
    history: trail([
      ['2026-01-01 09:00', 'admin', '프로젝트 등록 및 착수'],
    ]),
  },
  {
    id: 'PJT-006',
    code: 'PJT-2026-006',
    name: 'G사 클라우드 전환',
    client: 'G제조',
    status: 'RUNNING',
    startDate: '2026-02-01',
    endDate: '2026-08-31',
    memberCount: 1,
    desc: '레거시 시스템의 클라우드 네이티브 전환',
    members: [
      { empNo: 'BW-009', name: '임도현', role: '아키텍트', allocation: 100, type: 'RUNNING', startDate: '2026-02-01', endDate: '2026-08-31' },
    ],
    history: trail([
      ['2026-02-01 09:00', 'pm_lee', '프로젝트 등록 및 착수'],
    ]),
  },
  {
    id: 'PJT-007',
    code: 'PJT-2026-007',
    name: 'H사 데이터 플랫폼',
    client: 'H카드',
    status: 'PLANNED',
    startDate: '2026-10-01',
    endDate: '2027-06-30',
    memberCount: 0,
    desc: '전사 데이터 플랫폼 구축 (제안 진행중)',
    members: [],
    history: trail([
      ['2026-06-25 14:00', 'sales_jung', '제안서 작성 착수'],
    ]),
  },
  {
    id: 'PJT-008',
    code: 'PJT-2025-012',
    name: 'F사 SI 프로젝트',
    client: 'F통신',
    status: 'CLOSED',
    startDate: '2025-06-01',
    endDate: '2026-05-31',
    memberCount: 0,
    desc: '차세대 과금 시스템 SI 구축 (종료)',
    members: [],
    history: trail([
      ['2026-05-31 18:00', 'system', '프로젝트 종료 처리'],
    ]),
  },
]

export const assignments: Assignment[] = [
  { id: 'ASG-001', type: 'RUNNING', empNo: 'BW-011', name: '오세훈', projectName: 'A사 차세대 STO', role: 'PM', startDate: '2026-04-01', endDate: '2026-11-30', allocation: 100, status: 'ACTIVE', remark: '' },
  { id: 'ASG-002', type: 'RUNNING', empNo: 'BW-002', name: '김철수', projectName: 'A사 차세대 STO', role: 'Frontend Lead', startDate: '2026-04-01', endDate: '2026-09-30', allocation: 100, status: 'ACTIVE', remark: '' },
  { id: 'ASG-003', type: 'RUNNING', empNo: 'BW-004', name: '박민준', projectName: 'A사 차세대 STO', role: 'DB 설계', startDate: '2026-04-01', endDate: '2026-12-31', allocation: 80, status: 'ACTIVE', remark: '' },
  { id: 'ASG-004', type: 'COMMITTED', empNo: 'BW-009', name: '임도현', projectName: 'A사 차세대 STO', role: '아키텍트', startDate: '2026-09-01', endDate: '2026-12-31', allocation: 100, status: 'PLANNED', remark: 'G사 종료 후 투입 예정' },
  { id: 'ASG-005', type: 'RUNNING', empNo: 'BW-003', name: '이영희', projectName: 'B사 그룹웨어 고도화', role: '업무분석', startDate: '2026-05-01', endDate: '2026-11-30', allocation: 100, status: 'ACTIVE', remark: '' },
  { id: 'ASG-006', type: 'COMMITTED', empNo: 'BW-003', name: '이영희', projectName: 'C사 포털 재구축', role: '요건정의', startDate: '2026-08-01', endDate: '2026-12-31', allocation: 60, status: 'PLANNED', remark: '10월 투입률 합계 160% 초과' },
  { id: 'ASG-007', type: 'RUNNING', empNo: 'BW-008', name: '윤서진', projectName: 'B사 그룹웨어 고도화', role: '인프라', startDate: '2026-05-01', endDate: '2026-08-31', allocation: 50, status: 'ACTIVE', remark: '' },
  { id: 'ASG-008', type: 'RUNNING', empNo: 'BW-010', name: '한지민', projectName: 'C사 포털 재구축', role: 'UI 디자인', startDate: '2026-06-01', endDate: '2026-09-14', allocation: 40, status: 'ACTIVE', remark: '' },
  { id: 'ASG-009', type: 'RUNNING', empNo: 'BW-005', name: '최수연', projectName: 'D사 디지털 전환 컨설팅', role: '수석 컨설턴트', startDate: '2026-03-01', endDate: '2027-02-28', allocation: 80, status: 'ACTIVE', remark: '' },
  { id: 'ASG-010', type: 'RUNNING', empNo: 'BW-013', name: '문가영', projectName: 'D사 디지털 전환 컨설팅', role: '컨설턴트', startDate: '2026-03-01', endDate: '2026-10-14', allocation: 50, status: 'ACTIVE', remark: '' },
  { id: 'ASG-011', type: 'RUNNING', empNo: 'BW-006', name: '정재원', projectName: 'E사 유지보수 사업', role: '사업관리', startDate: '2026-01-01', endDate: '2026-12-31', allocation: 80, status: 'ACTIVE', remark: '' },
  { id: 'ASG-012', type: 'RUNNING', empNo: 'BW-009', name: '임도현', projectName: 'G사 클라우드 전환', role: '아키텍트', startDate: '2026-02-01', endDate: '2026-08-31', allocation: 100, status: 'ACTIVE', remark: '' },
  { id: 'ASG-013', type: 'PROPOSED', empNo: 'BW-007', name: '강하늘', projectName: 'H사 데이터 플랫폼', role: '개발자', startDate: '2026-10-01', endDate: '2027-06-30', allocation: 100, status: 'PLANNED', remark: '제안 진행중' },
  { id: 'ASG-014', type: 'PROPOSED', empNo: 'BW-012', name: '서지우', projectName: 'H사 데이터 플랫폼', role: 'QA', startDate: '2026-10-01', endDate: '2027-06-30', allocation: 80, status: 'PLANNED', remark: '제안 진행중' },
]

export const availabilityRows: AvailabilityRow[] = [
  { kind: 'IMMEDIATE', empNo: 'BW-001', name: '홍길동', team: 'DELIVERY', jobType: 'PM, AA', skills: ['Java', 'Spring'], allocation: 0, availableDate: '즉시' },
  { kind: 'IMMEDIATE', empNo: 'BW-007', name: '강하늘', team: 'DELIVERY', jobType: '개발자', skills: ['Java', 'Spring', 'TypeScript'], allocation: 0, availableDate: '즉시' },
  { kind: 'IMMEDIATE', empNo: 'BW-012', name: '서지우', team: 'DELIVERY', jobType: 'QA', skills: ['Java', 'MySQL'], allocation: 0, availableDate: '즉시' },
  { kind: 'PARTIAL', empNo: 'BW-010', name: '한지민', team: 'DELIVERY', jobType: 'UI/UX 디자이너', skills: ['Figma', 'TypeScript'], allocation: 40, availableDate: '2026-09-15' },
  { kind: 'PARTIAL', empNo: 'BW-008', name: '윤서진', team: 'DELIVERY', jobType: 'DevOps', skills: ['Kubernetes', 'Jenkins', 'AWS'], allocation: 50, availableDate: '2026-09-01' },
  { kind: 'PARTIAL', empNo: 'BW-013', name: '문가영', team: 'SALES_PARTNER', jobType: '컨설턴트, BA', skills: ['BPR', '전략기획'], allocation: 50, availableDate: '2026-10-15' },
  { kind: 'TERM', empNo: 'BW-002', name: '김철수', team: 'DELIVERY', jobType: 'TA', skills: ['React', 'Node.js', 'AWS'], allocation: 100, availableDate: '2026-10-01' },
  { kind: 'TERM', empNo: 'BW-009', name: '임도현', team: 'DELIVERY', jobType: 'AA, TA', skills: ['Java', 'AWS', 'PostgreSQL'], allocation: 100, availableDate: '2026-08-31' },
  { kind: 'TERM', empNo: 'BW-004', name: '박민준', team: 'DELIVERY', jobType: 'DBA', skills: ['Oracle', 'PostgreSQL'], allocation: 80, availableDate: '2027-01-01' },
  { kind: 'TERM', empNo: 'BW-011', name: '오세훈', team: 'DELIVERY', jobType: 'PM', skills: ['Java', 'Oracle'], allocation: 100, availableDate: '2026-11-30' },
  { kind: 'TERM', empNo: 'BW-003', name: '이영희', team: 'DELIVERY', jobType: 'BA', skills: ['Figma', 'MySQL'], allocation: 160, availableDate: '2026-12-01' },
]

export const recommendations: RecommendationRow[] = [
  {
    rank: 1,
    name: '임도현',
    jobType: 'AA, TA',
    skills: ['Java', 'AWS', 'PostgreSQL'],
    allocation: 100,
    availableDate: '2026-09-01',
    reason: '직무·기술 완전 일치, 8월 말 가동 가능',
    score: 94,
    detail: { jobMatch: 100, skillMatch: 95, proficiency: 90, availability: 85, experience: 95, roleFit: 98 },
  },
  {
    rank: 2,
    name: '홍길동',
    jobType: 'PM, AA',
    skills: ['Java', 'Spring'],
    allocation: 0,
    availableDate: '즉시',
    reason: '즉시 가동 가능, 아키텍트 경험 풍부',
    score: 89,
    detail: { jobMatch: 90, skillMatch: 85, proficiency: 92, availability: 100, experience: 88, roleFit: 80 },
  },
  {
    rank: 3,
    name: '강하늘',
    jobType: '개발자',
    skills: ['Java', 'Spring', 'TypeScript'],
    allocation: 0,
    availableDate: '즉시',
    reason: '즉시 가동, 백엔드 기술 보유 (숙련도 보통)',
    score: 76,
    detail: { jobMatch: 70, skillMatch: 80, proficiency: 60, availability: 100, experience: 65, roleFit: 72 },
  },
]

export const systemUsers: SystemUser[] = [
  { id: 'U-001', loginId: 'admin', email: 'admin@bwware.co.kr', role: 'ADMIN', linkedEmployee: '-', lastLogin: '2026-07-01 09:12', status: 'ACTIVE' },
  { id: 'U-002', loginId: 'hr_mgr', email: 'hr@bwware.co.kr', role: 'HR_MGR', linkedEmployee: '최수연 (BW-005)', lastLogin: '2026-07-01 08:40', status: 'ACTIVE' },
  { id: 'U-003', loginId: 'pm_ohsh', email: 'ohsh@bwware.co.kr', role: 'PM', linkedEmployee: '오세훈 (BW-011)', lastLogin: '2026-06-30 18:22', status: 'ACTIVE' },
  { id: 'U-004', loginId: 'pm_lee', email: 'pmlee@bwware.co.kr', role: 'PM', linkedEmployee: '임도현 (BW-009)', lastLogin: '2026-06-30 17:05', status: 'ACTIVE' },
  { id: 'U-005', loginId: 'lead_kim', email: 'kimcs@bwware.co.kr', role: 'TEAM_LEAD', linkedEmployee: '김철수 (BW-002)', lastLogin: '2026-06-29 11:33', status: 'ACTIVE' },
  { id: 'U-006', loginId: 'exec_ceo', email: 'ceo@bwware.co.kr', role: 'EXEC', linkedEmployee: '-', lastLogin: '2026-06-28 09:00', status: 'ACTIVE' },
  { id: 'U-007', loginId: 'viewer01', email: 'viewer@bwware.co.kr', role: 'VIEWER', linkedEmployee: '-', lastLogin: '2026-05-10 14:20', status: 'INACTIVE' },
]

export const auditLogs: AuditLog[] = [
  {
    id: 'AL-001',
    at: '2026-07-01 10:23:14',
    user: 'admin',
    action: 'UPDATE',
    targetTable: 'HR_EMPL_MST',
    targetId: 'BW-001',
    clientIp: '10.0.12.34',
    before: { JIKMU_CD: 'DEVELOPER' },
    after: { JIKMU_CD: 'ARCHITECT' },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/126.0',
  },
  {
    id: 'AL-002',
    at: '2026-07-01 09:45:02',
    user: 'pm_park',
    action: 'CREATE',
    targetTable: 'PJT_ASGN_HIS',
    targetId: 'ASG-006',
    clientIp: '10.0.12.51',
    before: null,
    after: { EMPL_ID: 'BW-003', PJT_ID: 'PJT-003', ALLOC_RT: 60, ASGN_TYPE_CD: 'COMMITTED' },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0',
  },
  {
    id: 'AL-003',
    at: '2026-07-01 09:12:33',
    user: 'admin',
    action: 'LOGIN',
    targetTable: 'SYS_USER_MST',
    targetId: 'U-001',
    clientIp: '10.0.12.34',
    before: null,
    after: null,
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/126.0',
  },
  {
    id: 'AL-004',
    at: '2026-06-30 17:20:41',
    user: 'hr_mgr',
    action: 'IMPORT',
    targetTable: 'HR_EMPL_MST',
    targetId: '-',
    clientIp: '10.0.12.20',
    before: null,
    after: { rows: 12, source: 'ResourceManagement_v2.xlsx' },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/126.0',
  },
  {
    id: 'AL-005',
    at: '2026-06-30 15:02:18',
    user: 'admin',
    action: 'DELETE',
    targetTable: 'HR_SKILL_MST',
    targetId: 'SK-018',
    clientIp: '10.0.12.34',
    before: { SKILL_NM: 'EJB', USE_YN: true },
    after: { SKILL_NM: 'EJB', USE_YN: false },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/126.0',
  },
]

// 대시보드 집계 (조직 전체 70명 기준 요약값)
export const dashboardKpis = {
  totalEmployees: 70,
  immediate: 8,
  partial: 11,
  full: 51,
  endingThisMonth: 6,
  avgUtilization: 73.3,
}

export const headcountTrend = [
  { month: '25.07', total: 62, hires: 3, exits: 1 },
  { month: '25.08', total: 64, hires: 3, exits: 1 },
  { month: '25.09', total: 65, hires: 2, exits: 1 },
  { month: '25.10', total: 66, hires: 2, exits: 1 },
  { month: '25.11', total: 67, hires: 2, exits: 1 },
  { month: '25.12', total: 66, hires: 1, exits: 2 },
  { month: '26.01', total: 68, hires: 3, exits: 1 },
  { month: '26.02', total: 69, hires: 2, exits: 1 },
  { month: '26.03', total: 69, hires: 1, exits: 1 },
  { month: '26.04', total: 70, hires: 2, exits: 1 },
  { month: '26.05', total: 70, hires: 1, exits: 1 },
  { month: '26.06', total: 70, hires: 1, exits: 1 },
]

export const jobTypeDistribution = [
  { name: '아키텍트(AA)', value: 8 },
  { name: '기술아키텍트(TA)', value: 4 },
  { name: '비즈니스 애널리스트(BA)', value: 5 },
  { name: 'DBA', value: 6 },
  { name: '프로젝트 매니저(PM)', value: 7 },
  { name: '컨설턴트', value: 9 },
  { name: '사업관리', value: 5 },
]

export const deptUtilization = [
  { team: '딜리버리', value: 82 },
  { team: '세일즈파트너', value: 60 },
  { team: '영업', value: 50 },
]

export const orgUtilization = {
  running: 73.3,
  committed: 83.3,
  proposed: 85.0,
}

export const dataQuality = {
  skillMissing: 3,
  jobMissing: 5,
  overAllocation: 1,
}

export const endingThisMonth = [
  { name: '한지민', team: '딜리버리', project: 'C사 포털 재구축', endDate: '2026-09-14', allocation: 40 },
  { name: '김철수', team: '딜리버리', project: 'A사 차세대 STO', endDate: '2026-09-30', allocation: 100 },
  { name: '윤서진', team: '딜리버리', project: 'B사 그룹웨어 고도화', endDate: '2026-08-31', allocation: 50 },
  { name: '임도현', team: '딜리버리', project: 'G사 클라우드 전환', endDate: '2026-08-31', allocation: 100 },
]

export const recentEmployees = [
  { empNo: 'BW-014', name: '배준호', team: '딜리버리', hireDate: '2022-04-11', role: '개발자' },
  { empNo: 'BW-007', name: '강하늘', team: '딜리버리', hireDate: '2024-01-02', role: '개발자' },
  { empNo: 'BW-010', name: '한지민', team: '딜리버리', hireDate: '2023-03-02', role: 'UI/UX 디자이너' },
  { empNo: 'BW-003', name: '이영희', team: '딜리버리', hireDate: '2023-07-03', role: 'BA' },
]

// 월별 가동률 매트릭스 (리포트용)
export const utilizationMatrix = [
  { empNo: 'BW-011', name: '오세훈', team: '딜리버리', project: 'A사 차세대 STO', months: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100], avg: 100 },
  { empNo: 'BW-002', name: '김철수', team: '딜리버리', project: 'A사 차세대 STO', months: [80, 80, 100, 100, 100, 100, 100, 100, 100, 0, 0, 0], avg: 72 },
  { empNo: 'BW-003', name: '이영희', team: '딜리버리', project: 'B사/C사', months: [100, 100, 100, 100, 100, 100, 100, 160, 160, 60, 60, 60], avg: 105 },
  { empNo: 'BW-004', name: '박민준', team: '딜리버리', project: 'A사 차세대 STO', months: [80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80], avg: 80 },
  { empNo: 'BW-009', name: '임도현', team: '딜리버리', project: 'G사/A사', months: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100], avg: 100 },
  { empNo: 'BW-008', name: '윤서진', team: '딜리버리', project: 'B사 그룹웨어', months: [50, 50, 50, 50, 50, 50, 0, 0, 0, 0, 0, 0], avg: 25 },
  { empNo: 'BW-005', name: '최수연', team: '세일즈파트너', project: 'D사 컨설팅', months: [80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80], avg: 80 },
  { empNo: 'BW-013', name: '문가영', team: '세일즈파트너', project: 'D사 컨설팅', months: [50, 50, 50, 50, 50, 50, 50, 0, 0, 0, 0, 0], avg: 33 },
  { empNo: 'BW-006', name: '정재원', team: '영업', project: 'E사 유지보수', months: [80, 80, 80, 80, 80, 80, 0, 0, 0, 0, 0, 0], avg: 40 },
  { empNo: 'BW-007', name: '강하늘', team: '딜리버리', project: '(대기)', months: [100, 100, 100, 100, 100, 0, 0, 0, 0, 0, 0, 0], avg: 42 },
]

export const matrixMonths = [
  '25.07', '25.08', '25.09', '25.10', '25.11', '25.12',
  '26.01', '26.02', '26.03', '26.04', '26.05', '26.06',
]

export const skillDistributionTop10 = [
  { name: 'Java', count: 28 },
  { name: 'Spring', count: 25 },
  { name: 'Oracle', count: 20 },
  { name: 'React', count: 18 },
  { name: 'TypeScript', count: 16 },
  { name: 'MySQL', count: 15 },
  { name: 'Node.js', count: 14 },
  { name: 'PostgreSQL', count: 12 },
  { name: 'AWS', count: 11 },
  { name: 'Vue', count: 9 },
]
