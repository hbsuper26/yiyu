import sys
import os
sys.path.append(os.path.dirname(__file__))

from agent import generate_daily_articles
from build_dist import freezer

def main():
    print("========================================")
    print("🚀 开始调用 MiniMax AI Agent 生成今日文章...")
    print("========================================")
    
    try:
        # 1. 生成文章并存入数据库
        success_count = generate_daily_articles()
        if success_count <= 0:
            raise RuntimeError("未生成任何文章，请先检查 MiniMax 凭证配置。")
        print(f"\n✅ 文章生成完毕并已保存至数据库！本次新增 {success_count} 篇。")
        
        # 2. 重新打包静态文件
        print("\n📦 开始重新打包静态页面 (更新 dist 文件夹)...")
        freezer.freeze()
        print("✅ 打包完成！最新的页面已生成在 dist 目录下。")
        
        print("\n🎉 全部操作成功！您现在可以打开 Sourcetree 提交变更了。")
        return 0
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        raise

if __name__ == "__main__":
    raise SystemExit(main())
