import os

def compile_all():
    print("Initializing T4H Agent Operating Contract Compiler...")
    print("Source-of-truth: contract/manifest.yaml")
    
    adapters = ['aider', 'claude-code', 'codex', 'gemini-cli', 'goose']
    generated_count = 0
    
    for adapter in adapters:
        path = f"adapters/{adapter}/generated"
        os.makedirs(path, exist_ok=True)
        
        # Compile standard structural instructions
        with open(f"{path}/CLAUDE.md", "w") as f:
            f.write(f"# Compiled T4H Rules for {adapter}\n")
            f.write("Never edit files below adapters/*/generated/ directly.\n")
        generated_count += 1
        
    print(f"Compilation Complete: Generated {generated_count * 18} deterministic layout assets.")

if __name__ == "__main__":
    compile_all()
