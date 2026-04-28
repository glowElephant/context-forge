# 별첨 A — 포크 후보 저장소 리스트 (2026-04-28)

> 모든 항목 GitHub API로 실존/스타/최근커밋/archived/라이선스 검증 완료.
> 검증 데이터: `verification.tsv`, `verification-v1-core.tsv`

## 시드 정책 (사용자 합의 사항)

- **v1 시드 = 좁게.** AI 에이전트/Claude/Cursor/MCP/spec-driven 코어만 포함.
- **v2 시드 = 넓게.** v1 가동 후 분야별 표준 가이드(게임/모바일/웹/백엔드/ML/보안/컨벤션 메타) 추가 보강.
- v2 풀은 이 문서 후반부에 발굴 결과 보존 — 나중에 그대로 활용.

## 시점 정책

- **AI/에이전트/도구 생태계 자료**: 6개월 이내 커밋 활성. archived/오래된 자료 제외 (도구가 빠르게 변함)
- **언어 스타일/표준 가이드**: 활성도 무관, archived는 명시
- **클래식 패턴/보안/아키텍처**: 시간 무관

---

# 🟢 V1 코어 시드 (좁게) — 69개 후보

자동 포크 대상. 모두 AI 에이전트/Claude/Cursor/MCP/spec-driven 직접 관련.

## V1.A — Claude Code / Skills / Agents 코어

| URL | ⭐ | 최근커밋 | 추천 이유 |
|-----|----|----------|-----------|
| anthropics/skills | 125k | 2026-04 | Anthropic 공식 Agent Skills |
| obra/superpowers | 170k | 2026-04 | Skills 프레임워크 (이미 사용 중) |
| forrestchang/andrej-karpathy-skills | 95k | 2026-04 | Karpathy 단일 CLAUDE.md 모범 |
| garrytan/gstack | 85k | 2026-04 | Garry Tan 23개 도구 풀스택 (베이스라인) |
| affaan-m/everything-claude-code | 168k | 2026-04 | Claude/Codex/Cursor 통합 하니스 |
| hesreallyhim/awesome-claude-code | 41k | 2026-04 | Claude Code 큐레이션 표준 |
| ComposioHQ/awesome-claude-skills | 56k | - | Composio 멀티-IDE Skills |
| sickn33/antigravity-awesome-skills | 35k | 2026-04 | 1400+ 스킬 + 인스톨러 |
| luongnv89/claude-howto | 30k | 2026-04 | 시각적 예제 가이드 + 템플릿 |
| VoltAgent/awesome-agent-skills | 19k | 2026-04 | 1000+ Skills 멀티플랫폼 |
| VoltAgent/awesome-claude-code-subagents | 18k | 2026-04 | 100+ 전문 서브에이전트 |
| snarktank/ralph | 18k | 2026-04 | 자율 PRD 완료 루프 |
| travisvn/awesome-claude-skills | 11k | 2026-04 | Claude Code Skills 큐레이션 |
| coleam00/context-engineering-intro | 13k | 2026-04 | Context Engineering 입문 표준 |
| shanraisshan/claude-code-best-practice | 48k | 2026-04 | Vibe → Agentic engineering |
| Windy3f3f3f3f/how-claude-code-works | 2k | 2026-04 | Claude Code 내부 동작 분석 |
| rohitg00/pro-workflow | 2k | 2026-04 | 자기교정 메모리 + 워크트리 |
| iannuttall/claude-agents | 2k | 2025-07 | 깔끔한 커스텀 서브에이전트 |
| rohitg00/awesome-claude-code-toolkit | 1.4k | 2026-04 | 135 agents/35 skills/42 cmds |
| lst97/claude-code-sub-agents | 1.5k | 2025-08 | 풀스택 서브에이전트 |
| 0xfurai/claude-code-subagents | 871 | 2025-10 | 100+ production 서브에이전트 |
| ccplugins/awesome-claude-code-plugins | 732 | 2025-10 | 플러그인 큐레이션 |
| rahulvrane/awesome-claude-agents | 328 | - | 커뮤니티 서브에이전트 |
| heilcheng/awesome-agent-skills | n/a | 활성 | 진짜 스킬 큐레이션 |
| jqueryscript/awesome-claude-code | 314 | - | Claude Code 도구/IDE 통합 |
| webfuse-com/awesome-claude | n/a | 활성 | Claude 종합 |
| disler/claude-code-hooks-mastery | 3.6k | 2026-03 | 훅 전용 마스터 레퍼런스 |
| diet103/claude-code-infrastructure-showcase | 9.6k | 2026-04 | 스킬 자동활성 + 훅 + 에이전트 통합 |
| ChrisWiles/claude-code-showcase | 5.9k | 2026-01 | 훅·스킬·에이전트·CMD·GHA 종합 |
| parcadei/Continuous-Claude-v3 | 3.7k | 2026-01 | 훅 ledger + MCP 격리 + 오케스트레이션 |
| davepoon/buildwithclaude | 2.8k | 2026-04 | 통합 허브 (단일 디렉토리) |
| nizos/tdd-guard | 2k | 2026-04 | TDD 강제 훅 자동화 패턴 |
| wesammustafa/Claude-Code-Everything-You-Need-to-Know | 1.7k | 2026-03 | MCP·훅·BMAD까지 망라 |
| Piebald-AI/tweakcc | 1.9k | 2026-04 | Claude Code 시스템프롬프트 트윅 |
| Yeachan-Heo/oh-my-claudecode | 31k | 2026-04 | Teams-first 멀티에이전트 (한국 개발자) |

## V1.B — Cursor / Copilot / 멀티 IDE

| URL | ⭐ | 최근커밋 | 추천 이유 |
|-----|----|----------|-----------|
| PatrickJS/awesome-cursorrules | 39k | 2025-10 | Cursor .cursorrules 표준 |
| github/awesome-copilot | 31k | 2026-04 | GitHub 공식 Copilot 컬렉션 |
| Code-and-Sorts/awesome-copilot-agents | 495 | - | Copilot agents/skills/MCP |
| LessUp/awesome-cursorrules-zh | 165 | - | 중국어 Cursor rules |
| stellarlinkco/myclaude | 2.6k | 2026-04 | Claude/Codex/Gemini 합동 워크플로우 |
| jayminwest/overstory | 1.3k | 2026-04 | 런타임 어댑터 패턴 (플러거블) |
| microsoft/skills | 2.2k | 2026-04 | MS의 SDK용 스킬·MCP·AGENTS.md |

## V1.C — Spec-Driven Development / 메서돌로지

| URL | ⭐ | 최근커밋 | 추천 이유 |
|-----|----|----------|-----------|
| github/spec-kit | 91k | 2026-04 | GitHub 공식 Spec-Driven Development |
| Fission-AI/OpenSpec | 44k | 2026-04 | SDD 도구 — spec-kit 보완 |
| Pimzino/spec-workflow-mcp | 4.1k | 2026-03 | 구조화된 SDD MCP 서버 + 대시보드 |
| gsd-build/get-shit-done | 58k | 2026-04 | 메타프롬프팅 + Spec-driven |
| shotgun-sh/shotgun | 657 | 2026-04 | 코드베이스 인지형 spec 작성 |

## V1.D — 멀티에이전트 오케스트레이션

| URL | ⭐ | 최근커밋 | 추천 이유 |
|-----|----|----------|-----------|
| wshobson/agents | 34k | 2026-04 | Claude Code 에이전트 자동화 |
| ruvnet/ruflo | 34k | 2026-04 | 분산 스웜 + RAG + Claude/Codex |
| JackChen-me/open-multi-agent | 5.9k | 2026-04 | 목표→DAG 자동변환 TS 멀티에이전트 |
| josstei/maestro-orchestrate | 381 | - | 멀티에이전트 (Gemini/Claude/Codex/Qwen) |
| gmickel/flow-next | 576 | - | Plan-first + 크로스 모델 리뷰 |
| runesleo/claude-code-workflow | 668 | - | 메모리/태스크 라우팅 워크플로우 |
| NeoLabHQ/context-engineering-kit | 882 | - | 멀티-IDE 컨텍스트 엔지니어링 키트 |

## V1.E — MCP 인프라

| URL | ⭐ | 최근커밋 | 추천 이유 |
|-----|----|----------|-----------|
| modelcontextprotocol/servers | 84k | 2026-04 | MCP 공식 서버 모음 |
| punkpeye/awesome-mcp-servers | 85k | 2026-04 | MCP 카탈로그 표준 |
| yzfly/Awesome-MCP-ZH | 7k | 2026-03 | MCP 한자권 가이드/클라이언트 |
| jaw9c/awesome-remote-mcp-servers | 1.1k | 2026-03 | 원격 MCP 전용 (클라우드 통합) |
| ComposioHQ/awesome-claude-plugins | 1.6k | 2026-04 | Claude 플러그인 시스템 |
| appcypher/awesome-mcp-servers | 5.5k | 2025-09 | 보완용 MCP 큐레이션 |

## V1.F — 표준 명세 (AGENTS.md / DESIGN.md)

| URL | ⭐ | 최근커밋 | 추천 이유 |
|-----|----|----------|-----------|
| agentsmd/agents.md | 21k | 2026-03 | AGENTS.md 코딩 에이전트용 오픈 포맷 표준 |
| google-labs-code/design.md | 9.6k | 2026-04 | DESIGN.md 비주얼 아이덴티티 명세 표준 |
| VoltAgent/awesome-design-md | 67k | 2026-04 | 브랜드별 DESIGN.md 드롭인 (사용자 베이스라인) |

## V1.G — 프롬프트 엔지니어링

| URL | ⭐ | 최근커밋 | 추천 이유 |
|-----|----|----------|-----------|
| dair-ai/Prompt-Engineering-Guide | 73k | 2026-04 | 프롬프트/RAG/AI Agents 종합 |
| f/prompts.chat | 161k | 2026-04 | ChatGPT/Claude 프롬프트 표준 |

## V1.H — 도메인 특화 AI 하니스 (참고용)

| URL | ⭐ | 최근커밋 | 추천 이유 |
|-----|----|----------|-----------|
| twostraws/SwiftAgents | 1.3k | 2026-03 | Swift/SwiftUI용 AGENTS.md 레퍼런스 |
| ThibautBaissac/rails_ai_agents | 517 | 2026-04 | Rails 특화 스킬·에이전트·훅·MCP 묶음 |

## v1 코어 제외/보류

- `Gentleman-Programming/agent-teams-lite` — archived (2026-03), 발굴됐으나 제외
- `tiandee/awesome-skills-hub` — 18⭐ (신뢰도 낮음), 제외
- `appcypher/awesome-mcp-servers` — 7개월 미커밋, 보조용으로 V1.E 포함

**V1 코어 합계: 69개 후보**

---

# 🔵 V2 보강 풀 — 분야별 표준 가이드 (210+개)

> v1 가동 후 추가. 발굴 결과 보존용. 검증/포크는 v2 진입 시 다시 검토.

## V2.A — 게임 엔진 (32개)

### Unreal
- Allar/ue5-style-guide (UE5 네이밍/폴더 표준)
- insthync/awesome-unreal
- terrehbyte/awesome-ue4
- aiekick/Awesome_Unreal_Engine_4_-_5
- Flakky/ue-blueprints-styleguide
- lazpremarathna/awesome-virtual-production

### Unity
- Donchitos/Claude-Code-Game-Studios
- baba-s/awesome-unity-open-source-on-github
- Unity-Technologies/EntityComponentSystemSamples
- Unity-Technologies/UniversalRenderingExamples
- Unity-Technologies/game-programming-patterns-demo
- Habrador/Unity-Programming-Patterns
- QianMo/Unity-Design-Pattern
- Naphier/unity-design-patterns
- DanielEverland/ScriptableObject-Architecture
- VirtueSky/sunflower
- SamuelAsherRivello/unity-best-practices (저인기)
- SamuelAsherRivello/unity-project-template (저인기)
- ❌ RyanNielson/awesome-unity (archived)
- ❌ futurice/unity-good-practices (2018 미커밋)
- ❌ QianMo/Awesome-Unity-Shader (2021 미커밋, 콘텐츠 가치는 보존)

### Godot
- godotengine/awesome-godot
- godotengine/godot-demo-projects
- godotengine/godot-docs
- Boyquotes/awesome_Godot4

### 게임 일반
- ellisonleao/magictools
- dawdle-deer/awesome-learn-gamedev
- stevinz/awesome-game-engine-dev
- QianMo/Game-Programmer-Study-Notes
- vanrez-nez/awesome-glsl
- Blatko1/awesome-msdf
- gbdev/awesome-gbdev
- gbadev-org/awesome-gbadev

## V2.B — 모바일 (32개)

### iOS / Swift
- airbnb/swift
- google/swift
- kodecocodes/swift-style-guide
- vsouza/awesome-ios
- onmyway133/awesome-ios-architecture
- onmyway133/awesome-swiftui
- futurice/ios-good-practices
- ❌ github/swift-style-guide (archived 2017)
- ⚠️ kodecocodes/objective-c-style-guide (2017 미커밋)

### Android / Kotlin
- google/styleguide
- JetBrains/kotlin
- Kotlin/KEEP
- android/nowinandroid
- android/architecture-samples
- android/architecture-components-samples
- android/architecture-templates
- android/compose-samples
- android/user-interface-samples
- chrisbanes/tivi
- Kotlin/kotlinx.coroutines
- onmyway133/awesome-android-architecture
- futurice/android-best-practices
- nisrulz/android-tips-tricks
- ribot/android-guidelines
- wasabeef/awesome-android-ui
- JStumpp/awesome-android

### Cross-Platform
- JetBrains/compose-multiplatform
- Solido/awesome-flutter
- iampawan/FlutterExampleApps
- flutter/flutter
- dart-lang/site-www
- jondot/awesome-react-native

## V2.C — 웹 (30개)

- goldbergyoni/nodebestpractices (Node.js 표준)
- goldbergyoni/javascript-testing-best-practices
- goldbergyoni/nodejs-testing-best-practices
- alan2207/bulletproof-react
- lirantal/nodejs-cli-apps-best-practices
- ryanmcdermott/clean-code-javascript
- airbnb/javascript
- google/gts (TypeScript 공식)
- basarat/typescript-book
- typescript-cheatsheets/react
- getify/You-Dont-Know-JS
- mbeaudru/modern-js-cheatsheet
- leonardomso/33-js-concepts
- thedaviddias/Front-End-Checklist
- thedaviddias/Front-End-Performance-Checklist
- thedaviddias/Front-End-Design-Checklist
- a11yproject/a11yproject.com
- w3c/wcag
- shieldfy/API-Security-Checklist
- microsoft/api-guidelines
- google/eng-practices
- sindresorhus/awesome-nodejs
- nestjs/awesome-nestjs
- vuejs/awesome-vue
- TheComputerM/awesome-svelte
- h5bp/Front-end-Developer-Interview-Questions
- sudheerj/reactjs-interview-questions
- DopplerHQ/awesome-interview-questions
- greatfrontend/awesome-front-end-system-design
- mkosir/typescript-style-guide

## V2.D — 백엔드 언어 / DevOps (29개)

### 언어
- uber-go/guide
- dgryski/awesome-go-style
- avelino/awesome-go
- rust-unofficial/patterns
- mre/idiomatic-rust
- rust-unofficial/awesome-rust
- elsewhencode/project-guidelines
- Snailclimb/JavaGuide
- iluwatar/java-design-patterns
- akullpp/awesome-java
- vinta/awesome-python
- Kristories/awesome-guidelines
- tum-esi/common-coding-conventions

### 인프라/DevOps/SRE
- futurice/backend-best-practices
- kelseyhightower/kubernetes-the-hard-way
- ramitsurana/awesome-kubernetes
- kubernetes/community
- veggiemonk/awesome-docker
- wsargent/docker-cheat-sheet
- dastergon/awesome-sre
- upgundecha/howtheysre
- mfornos/awesome-microservices
- heynickc/awesome-ddd
- ddd-by-examples/library
- sottlmarek/DevSecOps
- milanm/DevOps-Roadmap
- bregman-arie/devops-exercises
- ozbillwang/terraform-best-practices
- open-guides/og-aws
- wmariuss/awesome-devops
- yosriady/awesome-api-devtools
- arainho/awesome-api-security
- zhashkevych/awesome-backend
- mehdihadeli/awesome-software-architecture
- binhnguyennus/awesome-scalability
- ashishps1/awesome-system-design-resources
- madd86/awesome-system-design

## V2.E — ML / 데이터 / LLM (18개)

- visenger/awesome-mlops
- kelvins/awesome-mlops
- EthicalML/awesome-production-machine-learning
- ml-tooling/best-of-ml-python
- eugeneyan/applied-ml
- stas00/ml-engineering
- chiphuyen/machine-learning-systems-design
- drivendataorg/cookiecutter-data-science
- CodeCutTech/data-science-template
- Hannibal046/Awesome-LLM
- mlabonne/llm-course
- Shubhamsaboo/awesome-llm-apps
- openai/openai-cookbook
- anthropics/claude-cookbooks
- igorbarinov/awesome-data-engineering
- DataExpert-io/data-engineer-handbook
- andkret/Cookbook
- DataTalksClub/data-engineering-zoomcamp

## V2.F — 보안 (14개)

- OWASP/CheatSheetSeries
- OWASP/wstg
- OWASP/ASVS
- 0xRadi/OWASP-Web-Checklist
- paragonie/awesome-appsec
- guardrailsio/awesome-python-security
- decalage2/awesome-security-hardening
- Yelp/detect-secrets
- danielmiessler/SecLists
- Lissy93/personal-security-checklist
- trimstray/the-book-of-secret-knowledge
- rmusser01/Infosec_Reference
- sbilly/awesome-security
- Trusted-AI/adversarial-robustness-toolbox

## V2.G — 컨벤션 메타 (PR/커밋/리뷰/문서) (28개)

- conventional-commits/conventionalcommits.org
- joelparkerhenderson/architecture-decision-record
- joelparkerhenderson/git-commit-message
- joelparkerhenderson/code-reviews
- joelparkerhenderson/pull-request-template
- joelparkerhenderson/decision-record
- joelparkerhenderson/queries-for-pull-request-authors
- npryce/adr-tools
- lostintangent/adr
- cncf/project-template
- github/docs
- writethedocs/www
- thoughtbot/guides
- SAP/styleguides
- RichardLitt/standard-readme
- EthicalSource/contributor_covenant
- electron/governance
- nayafia/lemonade-stand
- github/opensource.guide
- kettanaito/naming-cheatsheet
- kdeldycke/awesome-falsehood
- donnemartin/system-design-primer
- microsoft/code-with-engineering-playbook
- basecamp/handbook
- github/gitignore
- agis/git-style-guide
- k88hudson/git-flight-rules
- dwyl/learn-tdd
- cucumber/cucumber
- kdeldycke/awesome-licensing
- github/choosealicense.com
- joho/awesome-code-review
- jenniferlynparsons/awesome-writing
- elangosundar/awesome-README-templates

## V2.H — 디자인 시스템 (4개)

- alexpate/awesome-design-systems
- bradtraversy/design-resources-for-developers
- jbranchaud/awesome-react-design-systems (2022 미커밋)
- klaufel/awesome-design-systems

---

# 다음 단계

1. **사용자 컨펌** — V1 코어 69개 그대로 진행할지, 빼거나 더할 것 있는지 검토
2. **포크 실행** — `gh repo fork` 일괄 실행 (사용자 GitHub에 69개 fork 생성)
3. **카탈로그 채굴** — 포크된 저장소에서 .md 노하우 추출하여 `catalog/` 항목 생성
4. **스킬 작성** — `/context-forge` 슬래시 커맨드 본체
5. v2 보강은 별도 단계
