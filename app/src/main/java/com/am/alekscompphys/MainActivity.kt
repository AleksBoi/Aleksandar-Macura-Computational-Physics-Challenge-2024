package com.am.alekscompphys

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material3.Button
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Slider
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.am.alekscompphys.ui.theme.AleksCompPhysTheme
import org.jetbrains.kotlinx.dataframe.api.columnOf
import org.jetbrains.kotlinx.dataframe.api.dataFrameOf
import org.jetbrains.kotlinx.kandy.dsl.plot
import org.jetbrains.kotlinx.kandy.letsplot.layers.line
import org.jetbrains.kotlinx.kandy.letsplot.settings.LineType
import org.jetbrains.kotlinx.kandy.letsplot.translator.toLetsPlot
import org.jetbrains.kotlinx.kandy.util.color.Color
import org.jetbrains.letsPlot.skia.compose.PlotPanel
import kotlin.math.cos
import kotlin.math.sin
import kotlin.math.sqrt

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            AleksCompPhysTheme {
                // A surface container using the 'background' color from the theme
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    var u by remember { mutableStateOf("") }
                    var g by remember { mutableStateOf("") }
                    var mass by remember { mutableStateOf("") }
                    var shape by remember { mutableStateOf("") }
                    var air_density by remember { mutableStateOf("") }
                    var CSA by remember { mutableStateOf("") }
                    var h by remember { mutableFloatStateOf(0f) }
                    var angle by remember { mutableFloatStateOf(0f) }
                    val xPositionsDrag = remember {
                        mutableStateListOf<Double>()
                    }
                    val yPositionsDrag = remember {
                        mutableStateListOf<Double>()
                    }
                    val xPositionsNoDrag = remember {
                        mutableStateListOf<Double>()
                    }
                    val yPositionsNoDrag = remember {
                        mutableStateListOf<Double>()
                    }

                    Column {
                        //Text (text = GetGraphValues(u.toFloat(),g.toFloat(),h,angle,shape.toFloat(),mass.toFloat(),air_density.toFloat(),CSA.toFloat()).toString())

                        val dataFrame = dataFrameOf(
                            columnOf(xPositionsNoDrag, yPositionsNoDrag),
                            columnOf(xPositionsDrag, yPositionsDrag)
                        )
                        val figure = dataFrame.plot {
                            line {
                                x(xPositionsNoDrag, "X Displacement")
                                y(yPositionsNoDrag, "Y Displacement")
                                width = 1.0
                                color = Color.RED
                                type = LineType.SOLID
                                alpha = 0.8
                            }
                            line {
                                x(xPositionsDrag, "X Displacement")
                                y(yPositionsDrag, "Y Displacement")
                                width = 1.0
                                color = Color.BLUE
                                type = LineType.SOLID
                                alpha = 0.8
                            }
                        }.toLetsPlot()
                        ElevatedCard(
                            modifier = Modifier.height(500.dp),
                            colors = CardDefaults.elevatedCardColors(
                                containerColor = androidx.compose.ui.graphics.Color.White
                            )
                        ) {
                            Text(
                                modifier = Modifier.padding(8.dp),
                                text = "Drag vs No Drag projectile motion",
                                style = MaterialTheme.typography.titleSmall
                            )
                            PlotPanel(
                                figure = figure,
                                modifier = Modifier.fillMaxSize()
                            ) { computationMessages ->
                                computationMessages.forEach { println("[DEMO APP MESSAGE] $it") }
                            }
                        }
                        Column {
                            Row {
                                TextField(
                                    modifier = Modifier
                                        .width(225.dp)
                                        .padding(
                                            start = 30.dp,
                                            end = 30.dp,
                                            top = 20.dp,
                                            bottom = 10.dp
                                        ),
                                    value = u,
                                    onValueChange = { u = it },
                                    label = { Text("Velocity") }
                                )
                                TextField(
                                    modifier = Modifier
                                        .width(225.dp)
                                        .padding(
                                            start = 30.dp,
                                            end = 30.dp,
                                            top = 20.dp,
                                            bottom = 10.dp
                                        ),
                                    value = g,
                                    onValueChange = { g = it },
                                    label = { Text("Gravity") }
                                )
                            }
                            Row {
                                TextField(
                                    modifier = Modifier
                                        .width(225.dp)
                                        .padding(
                                            start = 30.dp,
                                            end = 30.dp,
                                            top = 10.dp,
                                            bottom = 10.dp
                                        ),
                                    value = mass,
                                    onValueChange = { mass = it },
                                    label = { Text("Mass") }
                                )
                                TextField(
                                    modifier = Modifier
                                        .width(225.dp)
                                        .padding(
                                            start = 30.dp,
                                            end = 30.dp,
                                            top = 10.dp,
                                            bottom = 10.dp
                                        ),
                                    value = shape,
                                    onValueChange = { shape = it },
                                    label = { Text("Drag Coefficient") }
                                )
                            }
                            Row {
                                TextField(
                                    modifier = Modifier
                                        .width(225.dp)
                                        .padding(
                                            start = 30.dp,
                                            end = 30.dp,
                                            top = 10.dp,
                                            bottom = 10.dp
                                        ),
                                    value = air_density,
                                    onValueChange = { air_density = it },
                                    label = { Text("Air Density") }
                                )
                                TextField(
                                    modifier = Modifier
                                        .width(225.dp)
                                        .padding(
                                            start = 30.dp,
                                            end = 30.dp,
                                            top = 10.dp,
                                            bottom = 10.dp
                                        ),
                                    value = CSA,
                                    onValueChange = { CSA = it },
                                    label = { Text("CSA") }
                                )
                            }

                            Slider(
                                value = h,
                                valueRange = 0f..100f,
                                onValueChange = { h = it }
                            )
                            VariableDisplay(Variable = h, "Height")

                            Slider(
                                value = angle,
                                valueRange = 0f..90f,
                                onValueChange = { angle = it }
                            )
                            VariableDisplay(Variable = angle, "Angle")

                            Button(
                                modifier = Modifier.width(300.dp).align(Alignment.CenterHorizontally).padding(top = 25.dp).height(50.dp),
                                onClick = {
                                    //println((0.5f * shape.toFloat() * air_density.toFloat() * CSA.toFloat() / mass.toFloat()))
                                    val actualAngle = angle * 3.1415265f / 180f
                                    val timeIncrement = 0.01
                                    var currentTime = 0.0
                                    var currentYPosition = h
                                    var currentXPosition = 0.0


                                    while (currentYPosition > 0) {
                                        currentTime += timeIncrement

                                        currentXPosition = calculateXPosition(u.toDouble(), actualAngle.toDouble(), currentTime)
                                        currentYPosition = calculateYPosition(h.toDouble(), u.toDouble(), actualAngle.toDouble(), currentTime, g.toDouble())

                                        xPositionsNoDrag.add(currentXPosition)
                                        yPositionsNoDrag.add(currentYPosition.toDouble())
                                    }
                                    val dragConstant = (shape.toFloat() / mass.toFloat() * air_density.toFloat() * CSA.toFloat()) / 2.0
                                    currentTime = 0.0
                                    currentXPosition = 0.0
                                    currentYPosition = h
                                    var currentHorizontalVelocity = u.toFloat() * cos(actualAngle)
                                    var currentVerticalVelocity = u.toFloat() * sin(actualAngle)

                                    var currentVelocityMagnitude = u.toFloat()
                                    while (currentYPosition > 0) {
                                        val (newHorizontalAcceleration, newVerticalAcceleration) = calculateAccelerationDueToDrag(
                                            currentHorizontalVelocity.toDouble(),
                                            currentVerticalVelocity.toDouble(),
                                            dragConstant,
                                            g.toDouble(),
                                            currentVelocityMagnitude.toDouble()
                                        )
                                        val (newHorizontalVelocity, newVerticalVelocity) = calculateUpdatedVelocity(
                                            newHorizontalAcceleration to newVerticalAcceleration,
                                            currentHorizontalVelocity.toDouble(),
                                            currentVerticalVelocity.toDouble(),
                                            timeIncrement
                                        )
                                        val (newXPosition, newYPosition) = calculateDisplacement(
                                            newHorizontalVelocity to newVerticalVelocity,
                                            currentXPosition,
                                            currentYPosition.toDouble(),
                                            currentHorizontalVelocity.toDouble(),
                                            currentVerticalVelocity.toDouble(),
                                            newHorizontalAcceleration,
                                            newVerticalAcceleration,
                                            timeIncrement
                                        )

                                        xPositionsDrag.add(newXPosition)
                                        yPositionsDrag.add(newYPosition)

                                        currentHorizontalVelocity = newHorizontalVelocity.toFloat()
                                        currentVerticalVelocity = newVerticalVelocity.toFloat()
                                        currentTime += timeIncrement
                                        currentXPosition = newXPosition
                                        currentYPosition = newYPosition.toFloat()
                                        currentVelocityMagnitude =
                                            sqrt(currentHorizontalVelocity * currentHorizontalVelocity + currentVerticalVelocity * currentVerticalVelocity)
                                    }
                                }
                            ) {
                                Text("Press Here to Run")
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun VariableDisplay(Variable: Float, name: String){
    val thing = Variable.toString()
    Row{
        Text(
            text = "                "
        )
        Text(
            text = "Starting $name:"
        )
        Text(
            text = "                       "
        )
        Text(
            text = thing
        )
    }
}

private fun calculateAccelerationDueToDrag(
    horizontalVelocity: Double,
    verticalVelocity: Double,
    dragConstant: Double,
    gravitationalAcceleration: Double,
    velocityMagnitude: Double
): Pair<Double, Double> {
    val horizontalAcceleration = -1 * horizontalVelocity * dragConstant * velocityMagnitude
    val verticalAcceleration = -1 * gravitationalAcceleration - verticalVelocity * dragConstant * velocityMagnitude
    return horizontalAcceleration to verticalAcceleration
}

private fun calculateUpdatedVelocity(
    acceleration: Pair<Double, Double>,
    horizontalVelocity: Double,
    verticalVelocity: Double,
    timeIncrement: Double
): Pair<Double, Double> {
    val newHorizontalVelocity = horizontalVelocity + acceleration.first * timeIncrement
    val newVerticalVelocity = verticalVelocity + acceleration.second * timeIncrement
    return newHorizontalVelocity to newVerticalVelocity
}

private fun calculateDisplacement(
    velocity: Pair<Double, Double>,
    initialXPosition: Double,
    initialYPosition: Double,
    initialHorizontalVelocity: Double,
    initialVerticalVelocity: Double,
    horizontalAcceleration: Double,
    verticalAcceleration: Double,
    timeIncrement: Double
): Pair<Double, Double> {
    val newXPosition =
        initialXPosition + initialHorizontalVelocity * timeIncrement + 0.5 * horizontalAcceleration * timeIncrement * timeIncrement
    val newYPosition =
        initialYPosition + initialVerticalVelocity * timeIncrement + 0.5 * verticalAcceleration * timeIncrement * timeIncrement
    return newXPosition to newYPosition
}

private fun calculateXPosition(
    initialVelocity: Double,
    launchAngle: Double,
    timeElapsed: Double
): Double {
    return initialVelocity * cos(launchAngle) * timeElapsed
}

private fun calculateYPosition(
    initialHeight: Double,
    initialVelocity: Double,
    launchAngle: Double,
    timeElapsed: Double,
    gravitationalAcceleration: Double
): Float {
    return (initialHeight + initialVelocity * sin(launchAngle) * timeElapsed - 0.5 * gravitationalAcceleration * timeElapsed * timeElapsed).toFloat()
}

