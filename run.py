#!/usr/bin/env python3
import sys
import os
from app.bot import main

if __name__ == "__main__":
    # Создаем необходимые директории
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    main()