package com.example.shootergame

import android.content.Context
import android.graphics.*
import android.util.AttributeSet
import android.view.MotionEvent
import android.view.SurfaceHolder
import android.view.SurfaceView
import kotlin.random.Random

class ShooterGame @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null
) : SurfaceView(context, attrs), SurfaceHolder.Callback, Runnable {

    private var gameThread: Thread? = null
    private var isRunning = false
    private val paint = Paint()
    private var screenWidth = 0
    private var screenHeight = 0
    
    // 游戏对象
    private val player = Player()
    // 使用线程安全的集合
    private val bullets = Collections.synchronizedList(mutableListOf<Bullet>())
    private val enemies = Collections.synchronizedList(mutableListOf<Enemy>())
    private val explosions = Collections.synchronizedList(mutableListOf<Explosion>())

    // 颜色定义
    private val colors = object {
        val WHITE = Color.WHITE
        val BLACK = Color.BLACK
        val RED = Color.RED
        val YELLOW = Color.YELLOW
        val ORANGE = Color.rgb(255, 165, 0)
    }

    init {
        holder.addCallback(this)
        paint.isAntiAlias = true
    }

    // 玩家类
    inner class Player {
        var x = 0f
        var y = 0f
        val width = 100f
        val height = 100f
        val speed = 15f
        private var lastShootTime = 0L
        private val shootInterval = 500L  // 发射间隔时间（毫秒）

        fun update() {
            val currentTime = System.currentTimeMillis()
            if (currentTime - lastShootTime >= shootInterval) {
                shoot()
                lastShootTime = currentTime
            }
        }

        fun draw(canvas: Canvas) {
            paint.color = colors.WHITE
            canvas.drawRect(x, y, x + width, y + height, paint)
        }

        private fun shoot() {
            synchronized(gameLock) {
                if (bullets.size < 50) {  // 限制最大子弹数量
                    bulletPool.obtain().apply {
                        init(x + width/2, y, -1)
                        bullets.add(this)
                    }
                    bulletPool.obtain().apply {
                        init(x + width/2, y, 0)
                        bullets.add(this)
                    }
                    bulletPool.obtain().apply {
                        init(x + width/2, y, 1)
                        bullets.add(this)
                    }
                }
            }
        }
    }

    private fun updateGame() {
        synchronized(gameLock) {
            // 更新玩家（添加这行）
            player.update()

            // 更新子弹
            bullets.toList().forEach { bullet ->
                bullet.update()
                if (bullet.y < -bullet.height) {
                    bullets.remove(bullet)
                    bulletPool.recycle(bullet)
                }
            }

            // 更新敌人
            enemies.toList().forEach { it.update() }

            // 更新爆炸效果
            explosions.toList().forEach { explosion ->
                if (!explosion.update()) {
                    explosions.remove(explosion)
                }
            }

            // 碰撞检测
            checkCollisions()
        }
    }

    // 修改碰撞检测
    // 敌人类
        inner class Enemy {
            var x: Float = 0f
            var y: Float = -100f
            val width = 80f
            val height = 80f
            var speed: Float = 0f
            var type: String = ""
    
            init {
                reset()
            }
    
            fun init() {
                reset()  // 重用对象时重置状态
            }
    
            fun reset() {
                x = Random.nextFloat() * (screenWidth - width)
                y = -100f
                speed = Random.nextFloat() * 10f + 5f
                type = listOf("owl", "dog", "cat").random()
            }
        }

    // 在类的顶部添加分数相关变量
    private var score = 0
    private var isGameOver = false
    private val scoreMap = mapOf(
        "owl" to 2,
        "dog" to 3,
        "cat" to 5
    )

    // 添加绘制分数的方法
    private fun drawScore(canvas: Canvas) {
        paint.apply {
            color = colors.WHITE
            textSize = 50f
            textAlign = Paint.Align.LEFT
        }
        canvas.drawText("分数: $score", 20f, 60f, paint)
    }

    // 修改 drawGame 方法
    private fun drawGame() {
        val canvas = holder.lockCanvas() ?: return
        try {
            canvas.drawColor(colors.BLACK)
            synchronized(gameLock) {
                if (!isGameOver) {
                    player.draw(canvas)
                    bullets.toList().forEach { it.draw(canvas) }
                    enemies.toList().forEach { it.draw(canvas) }
                    explosions.toList().forEach { it.draw(canvas) }
                    drawScore(canvas)
                } else {
                    drawGameOver(canvas)
                }
            }
        } finally {
            holder.unlockCanvasAndPost(canvas)
        }
    }

    // 添加游戏结束界面
    private fun drawGameOver(canvas: Canvas) {
        paint.apply {
            textAlign = Paint.Align.CENTER
            color = colors.WHITE
        }

        // 绘制标题
        paint.textSize = 80f
        canvas.drawText("游戏结束", screenWidth/2f, screenHeight/3f, paint)

        // 绘制分数
        paint.textSize = 60f
        canvas.drawText("最终得分: $score", screenWidth/2f, screenHeight/2f, paint)

        // 绘制提示
        paint.textSize = 40f
        canvas.drawText("点击屏幕重新开始", screenWidth/2f, screenHeight * 2/3f, paint)
    }

    // 修改碰撞检测中的得分逻辑
    private fun checkCollisions() {
        synchronized(gameLock) {
            // 子弹击中敌人
            val bulletsToRemove = mutableListOf<Bullet>()
            val enemiesToRemove = mutableListOf<Enemy>()

            enemies.forEach { enemy ->
                bullets.forEach { bullet ->
                    if (isCollision(bullet, enemy)) {
                        bulletsToRemove.add(bullet)
                        enemiesToRemove.add(enemy)
                        score += scoreMap[enemy.type] ?: 0  // 增加分数
                        explosionPool.obtain().apply {
                            init(enemy.x + enemy.width/2, enemy.y + enemy.height/2)
                            explosions.add(this)
                        }
                    }
                }
            }

            // 批量处理移除操作
            bulletsToRemove.forEach { 
                bullets.remove(it)
                bulletPool.recycle(it)
            }
            enemiesToRemove.forEach { 
                enemies.remove(it)
                enemyPool.recycle(it)
                enemies.add(enemyPool.obtain())
            }

            // 敌人撞到玩家
            enemies.toList().forEach { enemy ->
                if (isCollision(player, enemy)) {
                    isGameOver = true
                    explosions.add(Explosion(player.x + player.width/2, player.y + player.height/2))
                }
            }
        }
    }

    // 修改触摸事件，添加重新开始功能
    override fun onTouchEvent(event: MotionEvent): Boolean {
        when (event.action) {
            MotionEvent.ACTION_DOWN -> {
                if (isGameOver) {
                    restartGame()
                    return true
                }
            }
            MotionEvent.ACTION_MOVE -> {
                if (!isGameOver) {
                    synchronized(gameLock) {
                        player.x = event.x - player.width/2
                        if (player.x < 0) player.x = 0f
                        if (player.x > screenWidth - player.width) {
                            player.x = screenWidth - player.width
                        }
                    }
                }
            }
        }
        return true
    }

    // 添加重新开始游戏的方法
    private fun restartGame() {
        synchronized(gameLock) {
            score = 0
            isGameOver = false
            isRunning = true
            
            // 清理所有游戏对象
            bullets.clear()
            enemies.clear()
            explosions.clear()

            // 重置玩家位置
            player.x = screenWidth/2f - player.width/2
            player.y = screenHeight - player.height - 20

            // 重新初始化敌人
            repeat(8) {
                enemies.add(Enemy())
            }

            // 重新启动游戏线程
            gameThread = Thread(this).apply { start() }
        }
    }

    private fun isCollision(obj1: Any, obj2: Any): Boolean {
        val (x1, y1, w1, h1) = when (obj1) {
            is Player -> listOf(obj1.x, obj1.y, obj1.width, obj1.height)
            is Bullet -> listOf(obj1.x, obj1.y, obj1.width, obj1.height)
            is Enemy -> listOf(obj1.x, obj1.y, obj1.width, obj1.height)
            else -> return false
        }
        val (x2, y2, w2, h2) = when (obj2) {
            is Player -> listOf(obj2.x, obj2.y, obj2.width, obj2.height)
            is Bullet -> listOf(obj2.x, obj2.y, obj2.width, obj2.height)
            is Enemy -> listOf(obj2.x, obj2.y, obj2.width, obj2.height)
            else -> return false
        }
        return !(x1 + w1 < x2 || x2 + w2 < x1 || y1 + h1 < y2 || y2 + h2 < y1)
    }
}