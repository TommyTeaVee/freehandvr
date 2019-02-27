using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class rightHand : MonoBehaviour
{
    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";
    string str5 = "";
    string str6 = "";

    static function basicSendRecieve()
    {
        str1 = "";
        str2 = "";
        str3 = "";
        str4 = "";
        str5 = "";
        str6 = "";
        //import stuff here

        //   CopyTransformsRecurse(curSrc, child);
    }
}
    public Rigidbody rb;
    private GameObject MainCamera;
    int xoff = 0;
    int yoff = 0;
    int zoff = 0;
    void Awake()
    {
        MainCamera = GameObject.FindGameObjectWithTag("Player");
    }
    // Start is called before the first frame update
    void Start()
    {
        UnityEngine.XR.XRSettings.eyeTextureResolutionScale = 2.0f;
        rb = GetComponent<Rigidbody>();
    }

    // Update is called once per frame
    void Update()
    {
        //xoff = 0;
       // yoff = 0;
        //zoff = 0;
        //import stuff here

        //
        //Vector3 newPos = new Vector3(MainCamera.transform.position.x + xoff, MainCamera.transform.position.y + yoff, MainCamera.transform.position.z + zoff);
       // rb.velocity = new Vector3(0f, 0f, 0f);
       // rb.angularVelocity = new Vector3(0f, 0f, 0f);
       // transform.position = newPos;
    }
}
