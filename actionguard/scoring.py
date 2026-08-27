from collections import Counter
WEIGHTS={'critical':25,'high':15,'medium':8,'low':3,'info':1}
CATEGORIES={'cicd':'cicd','agentic':'cicd','secrets':'secrets','artifacts':'artifacts','code_quality':'code_quality','dependencies':'dependencies','hygiene':'hygiene'}
def calculate_scores(findings):
    def score(items):
        tot=0
        for f in items:
            sev=f.severity.value if hasattr(f,'severity') and hasattr(f.severity,'value') else (f.get('severity') if isinstance(f,dict) else str(getattr(f,'severity','')))
            tot+=WEIGHTS.get(sev,0)
        return max(0,100-tot)
    scores={'overall':score(findings)}
    for out in ['cicd','secrets','artifacts','code_quality','dependencies','hygiene']:
        scores[out]=score([f for f in findings if CATEGORIES.get(f.category if hasattr(f,'category') else f.get('category'))==out])
    return scores
def severity_counts(findings):
    def get_sev(f):
        return f.severity.value if hasattr(f,'severity') and hasattr(f.severity,'value') else (f.get('severity') if isinstance(f,dict) else str(getattr(f,'severity','')))
    c=Counter(get_sev(f) for f in findings); return {x:c.get(x,0) for x in WEIGHTS}
