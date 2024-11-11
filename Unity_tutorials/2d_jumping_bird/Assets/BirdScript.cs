using UnityEngine;

public class BirdScript : MonoBehaviour
{
    // References
    public Rigidbody2D birdRigidbody;
    public float jumpStrength;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space) == true) 
        {
            birdRigidbody.linearVelocity = Vector2.up * jumpStrength;
        }
 
    }
}
