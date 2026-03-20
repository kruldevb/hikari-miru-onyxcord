# 🚀 ModalBuilder - Declarative Modal API

O ModalBuilder é uma API declarativa e moderna para criar modais com os novos componentes do Discord de forma limpa e profissional.

## 🎯 Por que usar ModalBuilder?

### ❌ ANTES (Forma Antiga)

Você precisava de múltiplas variáveis:

```python
class MyModal(OnyxModal, title="Form"):
    name_input = TextInput(label="Name", custom_id="name")
    file_upload = FileUpload(custom_id="files", max=2)
    priority = RadioGroup(custom_id="priority", options=[...])
    features = CheckboxGroup(custom_id="features", options=[...])
    confirm = Checkbox(custom_id="confirm")
    
    async def callback(self, ctx):
        # Acessar cada variável individualmente
        name = self.name_input.value
        files = self.file_upload.attachments
        priority = self.priority.value
        # ...
```

### ✅ AGORA (ModalBuilder)

**UMA variável, TODOS os componentes:**

```python
class MyModal(OnyxModal, title="Form"):
    modal = ModalBuilder(
        Text(label="Name", custom_id="name", required=True),
        File(custom_id="files", max=2),
        Radio(custom_id="priority", options=[("Low", "low"), ("High", "high")]),
        CheckboxGroupField(custom_id="features", options=[("API", "api")]),
        CheckboxField(custom_id="confirm"),
    )
    
    async def callback(self, ctx):
        # Obter TODOS os valores com UMA linha!
        data = self.modal.get(self)
        
        # Acessar valores de forma limpa
        await ctx.respond(f"""
            Name: {data.name}
            Files: {len(data.files or [])}
            Priority: {data.priority}
            Features: {data.features}
            Confirmed: {data.confirm}
        """)
```

## 📦 Componentes Disponíveis

### 1. Text - Campo de Texto

```python
Text(
    label="Nome",
    custom_id="name",
    placeholder="Digite seu nome...",
    required=True,
    min_length=2,
    max_length=50,
    style=hikari.TextInputStyle.SHORT  # ou PARAGRAPH
)
```

### 2. File - Upload de Arquivos

```python
File(
    custom_id="files",
    label="Anexos",
    max=3,  # Máximo de arquivos
    required=False,
    file_types=["image/*", ".pdf", ".docx"]
)
```

### 3. Radio - Escolha Única

```python
Radio(
    custom_id="priority",
    label="Prioridade",
    options=[
        ("Baixa", "low"),
        ("Média", "medium"),
        ("Alta", "high"),
    ],
    required=True
)
```

### 4. CheckboxGroupField - Múltipla Escolha

```python
CheckboxGroupField(
    custom_id="features",
    label="Recursos",
    options=[
        ("API", "api"),
        ("UI", "ui"),
        ("Database", "db"),
    ],
    required=False
)
```

### 5. CheckboxField - Checkbox Individual

```python
CheckboxField(
    custom_id="agree",
    label="Eu concordo com os termos",
    required=True
)
```

## 🎨 Exemplos Completos

### Exemplo 1: Formulário de Feedback

```python
from miru.onyx import OnyxModal, ModalBuilder, Text, Radio, CheckboxField

class FeedbackModal(OnyxModal, title="Feedback"):
    modal = ModalBuilder(
        Text(
            label="Seu Nome",
            custom_id="name",
            placeholder="João Silva",
            required=True,
        ),
        Radio(
            custom_id="rating",
            label="Avaliação",
            options=[
                ("⭐ Ruim", "1"),
                ("⭐⭐ Regular", "2"),
                ("⭐⭐⭐ Bom", "3"),
                ("⭐⭐⭐⭐ Ótimo", "4"),
                ("⭐⭐⭐⭐⭐ Excelente", "5"),
            ],
            required=True,
        ),
        Text(
            label="Comentários",
            custom_id="comments",
            placeholder="Conte-nos mais...",
            style=hikari.TextInputStyle.PARAGRAPH,
        ),
        CheckboxField(
            custom_id="newsletter",
            label="Quero receber novidades",
        ),
    )
    
    async def callback(self, ctx):
        data = self.modal.get(self)
        
        stars = "⭐" * int(data.rating)
        newsletter = "Sim" if data.newsletter else "Não"
        
        await ctx.respond(
            f"Obrigado {data.name}!\n"
            f"Avaliação: {stars}\n"
            f"Comentários: {data.comments or 'Nenhum'}\n"
            f"Newsletter: {newsletter}",
            flags=hikari.MessageFlag.EPHEMERAL
        )
```

### Exemplo 2: Relatório de Bug

```python
class BugReportModal(OnyxModal, title="Reportar Bug"):
    modal = ModalBuilder(
        Text(
            label="Título do Bug",
            custom_id="title",
            placeholder="Descrição breve",
            required=True,
            max_length=100,
        ),
        Text(
            label="Passos para Reproduzir",
            custom_id="steps",
            placeholder="1. Vá para...\n2. Clique em...\n3. Veja o erro",
            style=hikari.TextInputStyle.PARAGRAPH,
            required=True,
        ),
        Radio(
            custom_id="severity",
            label="Gravidade",
            options=[
                ("Menor", "minor"),
                ("Moderado", "moderate"),
                ("Maior", "major"),
                ("Crítico", "critical"),
            ],
            required=True,
        ),
        File(
            custom_id="screenshot",
            label="Screenshot",
            max=2,
            file_types=["image/*"],
        ),
        CheckboxGroupField(
            custom_id="platforms",
            label="Plataformas Afetadas",
            options=[
                ("Windows", "windows"),
                ("macOS", "macos"),
                ("Linux", "linux"),
                ("Mobile", "mobile"),
            ],
        ),
    )
    
    async def callback(self, ctx):
        data = self.modal.get(self)
        
        embed = hikari.Embed(
            title=f"🐛 Bug: {data.title}",
            description=data.steps,
            color=hikari.Color(0xFF0000),
        )
        embed.add_field("Gravidade", data.severity.upper(), inline=True)
        embed.add_field(
            "Plataformas",
            ", ".join(data.platforms) if data.platforms else "Não especificado",
            inline=True
        )
        
        if data.screenshot:
            embed.add_field(
                "Screenshots",
                f"{len(data.screenshot)} arquivo(s) anexado(s)",
                inline=False
            )
            # Adicionar links para os arquivos
            for file in data.screenshot:
                embed.add_field(file.filename, file.url, inline=False)
        
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
```

### Exemplo 3: Formulário de Contato

```python
class ContactModal(OnyxModal, title="Contato"):
    modal = ModalBuilder(
        Text(
            label="Email",
            custom_id="email",
            placeholder="seu@email.com",
            required=True,
        ),
        Text(
            label="Assunto",
            custom_id="subject",
            placeholder="Sobre o que você quer falar?",
            required=True,
        ),
        Text(
            label="Mensagem",
            custom_id="message",
            placeholder="Sua mensagem aqui...",
            style=hikari.TextInputStyle.PARAGRAPH,
            required=True,
            max_length=1000,
        ),
        Radio(
            custom_id="department",
            label="Departamento",
            options=[
                ("Suporte", "support"),
                ("Vendas", "sales"),
                ("Geral", "general"),
            ],
        ),
    )
    
    async def callback(self, ctx):
        data = self.modal.get(self)
        
        await ctx.respond(
            f"✅ Mensagem enviada!\n\n"
            f"**Email:** {data.email}\n"
            f"**Assunto:** {data.subject}\n"
            f"**Departamento:** {data.department}\n"
            f"**Mensagem:** {data.message[:100]}...",
            flags=hikari.MessageFlag.EPHEMERAL
        )
```

## 🔧 Como Funciona Internamente

### 1. Definição

Quando você define `modal = ModalBuilder(...)`, você está criando uma lista de "fields" (campos).

### 2. Inicialização

Quando o modal é instanciado, o `__init__` do `OnyxModal` detecta automaticamente o `ModalBuilder` e chama `modal.build(self)`.

### 3. Build

O método `build()` itera sobre todos os fields e:
- Chama `field.build()` para criar o componente real
- Adiciona o componente ao modal com `modal.add_item()`
- Define um atributo no modal com `setattr(modal, field.custom_id, item)`

### 4. Submissão

Quando o usuário submete o modal:
- Os valores são parseados normalmente
- Você chama `data = self.modal.get(self)`
- O método `get()` extrai todos os valores e retorna um objeto `ModalData`

### 5. Acesso aos Dados

O objeto `ModalData` tem todos os valores como atributos:
```python
data.name       # Valor do campo "name"
data.files      # Lista de arquivos do campo "files"
data.priority   # Valor selecionado do radio "priority"
```

## 🎯 Benefícios

✅ **Código mais limpo**: Uma variável ao invés de múltiplas  
✅ **Mais legível**: Estrutura declarativa clara  
✅ **Type-safe**: Autocomplete e type hints funcionam  
✅ **Menos erros**: Menos variáveis = menos chance de erro  
✅ **Profissional**: API moderna estilo React/FastAPI  
✅ **Fácil manutenção**: Adicionar/remover campos é trivial  
✅ **Acesso unificado**: `data.field_name` para tudo  

## 🚀 Próximos Passos

Possíveis melhorias futuras:

- **Validação automática**: Validar campos antes do callback
- **Mensagens de erro**: Erro customizado por campo
- **Campos condicionais**: Mostrar campos baseado em outros
- **Auto-embed**: Gerar embed automaticamente dos dados
- **Serialização**: Salvar/carregar dados facilmente

## 📚 Veja Também

- `examples/modal_builder_example.py` - Exemplos completos
- `miru/onyx/fields.py` - Código fonte do ModalBuilder
- `miru/onyx/modal.py` - Integração com OnyxModal

---

**Desenvolvido por:** Gustavo S.  
**Inspirado por:** React Forms, Discord UI Builders, FastAPI
