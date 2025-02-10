import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class HelloWorldTest {

    @Test
    public void testMainMethod() {
        // Redirecting System.out to capture the output
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        PrintStream printStream = new PrintStream(outputStream);
        System.setOut(printStream);

        // Call the main method of HelloWorld
        HelloWorld.main(new String[]{});

        // Capture the output and assert it equals the expected output
        String expectedOutput = "Hello, World!\n";
        assertEquals(expectedOutput, outputStream.toString());
    }
}
