# System Architecture

```text
                    +----------------------+
                    | HR / IAM / ITSM      |
                    | Access Request       |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Identity Context     |
                    | Graph / Entra        |
                    +----------+-----------+
                               |
              +----------------+----------------+
              |                                 |
              v                                 v
     +------------------+              +------------------+
     | Access Analysis  |              | Risk Analysis    |
     +--------+---------+              +--------+---------+
              |                                 |
              +----------------+----------------+
                               v
                    +----------------------+
                    | AI Recommendation    |
                    | Advisory only        |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Deterministic Policy  |
                    | Security Gate         |
                    +----------+-----------+
                               |
                  +------------+------------+
                  |            |            |
                  v            v            v
               APPROVE       REVIEW       BLOCK
                  |            |            |
                  +------------+------------+
                               |
                               v
                    +----------------------+
                    | Human Approval       |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Graph / PowerShell   |
                    | Controlled Action    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Entra ID             |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Audit Evidence       |
                    +----------------------+
```

## Trust boundaries

1. External request -> validation
2. Entra -> identity context
3. AI -> untrusted recommendation
4. Policy engine -> authorization boundary
5. Human approval -> execution gate
6. Automation -> Entra
